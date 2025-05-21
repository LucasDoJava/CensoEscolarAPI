from os import read
from flask import Flask, jsonify, request, g
import _sqlite3
from marshmallow import ValidationError

from helpers.application import app
from helpers.database import getConnection
from helpers.logging import logger
from helpers.CORS import cors

from Models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchemas, UFSchema, MesorregiaoSchema, MicrorregiaoSchema, MunicipioSchema

cors.init_app(app)


@app.route("/")
def index():
    versao = {"versao": "0.0.1"}
    return (jsonify(versao), 200) 

@app.get("/instituicoes")
def instituicoesResource():
    logger.info("GET - Instituições com paginação")

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    offset = (page - 1) * per_page

    try:
        instituicoesEnsino = []

        cursor = getConnection().cursor()
        

        cursor.execute('SELECT * FROM tb_instituicao LIMIT ? OFFSET ?', (per_page, offset))
        resultSet = cursor.fetchall()

        for row in resultSet:
            instituicaoEnsino = InstituicaoEnsino(
                row[0], row[1], row[2], row[3],
                row[4], row[5], row[6], row[7],
                row[8]
            )
            instituicoesEnsino.append(instituicaoEnsino.toDict())

    except _sqlite3.Error:
        logger.error("Problema com banco")
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
 

    return jsonify(instituicoesEnsino), 200



@app.get("/instituicoes/<int:id>")
def instituicoesByIdResource(id):
    logger.info("Get - Instituições")
    try:
        cursor = getConnection().cursor()
        cursor.execute('SELECT regiao, codRegiao, UF, codUF, municipio, codMunicipio, entidade, codEntidade, matriculas_base FROM tb_instituicao WHERE codEntidade = ?', (id,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"mensagem": "Instituição não encontrada"}), 404

        instituicao = InstituicaoEnsino(*row)
        return jsonify(instituicao.toDict()), 200

    except _sqlite3.Error:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500


@app.post("/instituicoes")
def instituicaoInsercaoResource():
    logger.info("POST - Instituições")
    content = request.get_json()

    required_fields = [
        'regiao', 'codRegiao', 'UF', 'codUF', 'municipio', 'codMunicipio',
        'entidade', 'matriculas_base'
    ]

    if not all(field in content for field in required_fields):
        return jsonify({"mensagem": "Campos ausentes"}), 400

    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_instituicao (
                regiao, codRegiao, UF, codUF, municipio, codMunicipio,
                entidade, matriculas_base
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            content['regiao'], content['codRegiao'], content['UF'], content['codUF'],
            content['municipio'], content['codMunicipio'],
            content['entidade'], content['matriculas_base']
        ))

        conn.commit()
        codEntidade = cursor.lastrowid  

        nova_instituicao = InstituicaoEnsino(
            content['regiao'], content['codRegiao'], content['UF'], content['codUF'],
            content['municipio'], content['codMunicipio'],
            content['entidade'], codEntidade, content['matriculas_base']
        )

        return jsonify(nova_instituicao.toDict()), 201

    except _sqlite3.Error as e:
         logger.error("Erro ao inserir")
         return jsonify({"mensagem": f"Erro ao inserir: {str(e)}"}), 500
    
   


@app.put("/instituicoes/<int:id>")
def instituicaoAtualizacaoResource(id):
    logger.info("PUT - Instituições")
    content = request.get_json()

    required_fields = [
        'regiao', 'codRegiao', 'UF', 'codUF', 'municipio',
        'codMunicipio', 'entidade', 'matriculas_base'
    ]

    if not all(field in content for field in required_fields):
        logger.error("Campos ausentes")
        return jsonify({"mensagem": "Campos ausentes"}), 400

    try:
        conn = getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tb_instituicao SET
                regiao = ?, codRegiao = ?, UF = ?, codUF = ?, municipio = ?,
                codMunicipio = ?, entidade = ?, matriculas_base = ?
            WHERE codEntidade = ?
        """, (
            content['regiao'], content['codRegiao'], content['UF'], content['codUF'],
            content['municipio'], content['codMunicipio'], content['entidade'], content['matriculas_base'], id
        ))

        if cursor.rowcount == 0:
            logger.error("Instituição não encotrada")
            return jsonify({"mensagem": "Instituição não encontrada"}), 404

        conn.commit()
        content['codEntidade'] = id
        return jsonify(content), 200

    except _sqlite3.Error:
        logger.error("Erro ao atualizar")
        return jsonify({"mensagem": "Erro ao atualizar."}), 500
    

@app.delete("/instituicoes/<int:id>")
def instituicaoRemocaoResource(id):
    logger.info("DELETE - Instituições")
    try:
        conn = getConnection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tb_instituicao WHERE codEntidade = ?", (id,))

        if cursor.rowcount == 0:
            logger.error("Instituição não encontrada")
            return jsonify({"mensagem": "Instituição não encontrada"}), 404

        conn.commit()
        return jsonify({"mensagem": "Instituição removida com sucesso"}), 200

    except _sqlite3.Error:
        logger.error("Erro ao remover a instituição")
        return jsonify({"mensagem": "Erro ao remover instituição."}), 500
   

DB_FILE = "censoescolar.db"

@app.route('/instituicoess', methods=['GET'])
def get_instituicoes():
   
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page

    with _sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                i.codEntidade,
                i.entidade,
                i.codMunicipio,
                m.nomeMunicipio,
                i.codUF,
                uf.nomeEstado,
                mi.codMicrorregiao,
                mi.microrregiao,
                me.codMesorregiao,
                me.mesorregiao,
                i.matriculas_base
            FROM tb_instituicao i
            JOIN tb_Municipio m ON i.codMunicipio = m.idMunicipio
            JOIN tb_Microrregiao mi ON m.codMicrorregiao = mi.codMicrorregiao
            JOIN tb_Mesorregiao me ON m.codMesorregiao = me.codMesorregiao
            JOIN tb_UF uf ON i.codUF = uf.codUF
            LIMIT ? OFFSET ?;
        """, (per_page, offset))

        colunas = [desc[0] for desc in cursor.description]
        resultados = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
