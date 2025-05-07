from os import read
from flask import Flask, jsonify, request
import json
import os
from Models.InstituicaoEnsino import InstituicaoEnsino
import _sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    versao = {"versao": "0.0.1"}
    return (jsonify(versao), 200) 

@app.get("/instituicoes")
def instituicoesResource():
    print("GET - Instituições com paginação")

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    offset = (page - 1) * per_page

    try:
        instituicoesEnsino = []

        conn = _sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM tb_instituicao LIMIT ? OFFSET ?', (per_page, offset))
        resultSet = cursor.fetchall()

        for row in resultSet:
            instituicaoEnsino = InstituicaoEnsino(
                row[0], row[1], row[2], row[3],
                row[4], row[5], row[6], row[7],
                row[8], row[9], row[10], row[11],
                row[12]
            )
            instituicoesEnsino.append(instituicaoEnsino.toDict())

    except _sqlite3.Error:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()

    return jsonify(instituicoesEnsino), 200



@app.get("/instituicoes/<int:id>")
def instituicoesByIdResource(id):
    try:
        conn = _sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute('SELECT regiao, codRegiao, UF, codUF, municipio, codMunicipio, mesoregiao, codMesoregiao, microregiao, codMicroregiao, entidade, codEntidade, matriculas_base FROM tb_instituicao WHERE codEntidade = ?', (id,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"mensagem": "Instituição não encontrada"}), 404

        instituicao = InstituicaoEnsino(*row)
        return jsonify(instituicao.toDict()), 200

    except _sqlite3.Error:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()


@app.post("/instituicoes")
def instituicaoInsercaoResource():
    content = request.get_json()

    required_fields = [
        'regiao', 'codRegiao', 'UF', 'codUF', 'municipio', 'codMunicipio',
        'mesoregiao', 'codMesoregiao', 'microregiao', 'codMicroregiao',
        'entidade', 'matriculas_base'
    ]

    if not all(field in content for field in required_fields):
        return jsonify({"mensagem": "Campos ausentes"}), 400

    try:
        conn = _sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_instituicao (
                regiao, codRegiao, UF, codUF, municipio, codMunicipio,
                mesoregiao, codMesoregiao, microregiao, codMicroregiao,
                entidade, matriculas_base
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            content['regiao'], content['codRegiao'], content['UF'], content['codUF'],
            content['municipio'], content['codMunicipio'], content['mesoregiao'],
            content['codMesoregiao'], content['microregiao'], content['codMicroregiao'],
            content['entidade'], content['matriculas_base']
        ))

        conn.commit()
        codEntidade = cursor.lastrowid  

        nova_instituicao = InstituicaoEnsino(
            content['regiao'], content['codRegiao'], content['UF'], content['codUF'],
            content['municipio'], content['codMunicipio'], content['mesoregiao'],
            content['codMesoregiao'], content['microregiao'], content['codMicroregiao'],
            content['entidade'], codEntidade, content['matriculas_base']
        )

        return jsonify(nova_instituicao.toDict()), 201

    except _sqlite3.Error as e:
        return jsonify({"mensagem": f"Erro ao inserir: {str(e)}"}), 500
    finally:
        conn.close()


@app.put("/instituicoes/<int:id>")
def instituicaoAtualizacaoResource(id):
    content = request.get_json()

    required_fields = [
        'regiao', 'codRegiao', 'UF', 'codUF', 'municipio',
        'codMunicipio', 'mesoregiao', 'codMesoregiao', 'microregiao',
        'codMicroregiao', 'entidade', 'matriculas_base'
    ]

    if not all(field in content for field in required_fields):
        return jsonify({"mensagem": "Campos ausentes"}), 400

    try:
        conn = _sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tb_instituicao SET
                regiao = ?, codRegiao = ?, UF = ?, codUF = ?, municipio = ?,
                codMunicipio = ?, mesoregiao = ?, codMesoregiao = ?, microregiao = ?,
                codMicroregiao = ?, entidade = ?, matriculas_base = ?
            WHERE codEntidade = ?
        """, (
            content['regiao'], content['codRegiao'], content['UF'], content['codUF'],
            content['municipio'], content['codMunicipio'], content['mesoregiao'], content['codMesoregiao'],
            content['microregiao'], content['codMicroregiao'], content['entidade'], content['matriculas_base'], id
        ))

        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Instituição não encontrada"}), 404

        conn.commit()
        content['codEntidade'] = id
        return jsonify(content), 200

    except _sqlite3.Error:
        return jsonify({"mensagem": "Erro ao atualizar."}), 500
    finally:
        conn.close()

@app.delete("/instituicoes/<int:id>")
def instituicaoRemocaoResource(id):
    try:
        conn = _sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tb_instituicao WHERE codEntidade = ?", (id,))

        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Instituição não encontrada"}), 404

        conn.commit()
        return jsonify({"mensagem": "Instituição removida com sucesso"}), 200

    except _sqlite3.Error:
        return jsonify({"mensagem": "Erro ao remover instituição."}), 500
    finally:
        conn.close()

