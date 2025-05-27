from flask import jsonify, request
from flask_restful import Resource, marshal
from marshmallow import ValidationError
import _sqlite3

from helpers.database import getConnection
from helpers.logging import logger

from Models.InstituicaoEnsino import InstituicaoEnsino, instituicao_fields

class InstituicoesResource(Resource):
    def get(self):

        logger.info("GET - Instituições com paginação")

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        offset = (page - 1) * per_page

        try:
            instituicoesEnsino = []

            conn = getConnection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM tb_instituicao LIMIT ? OFFSET ?', (per_page, offset))
            resultSet = cursor.fetchall()

            for row in resultSet:
                instituicaoEnsino = InstituicaoEnsino(
                    row[0], row[1], row[2], row[3],
                    row[4], row[5], row[6], row[7],
                    row[8]
                )
                instituicoesEnsino.append(instituicaoEnsino)

            cursor.close()
            conn.close()

        except _sqlite3.Error:
            logger.error("Problema com banco")
            return {"mensagem": "Problema com o banco de dados."}, 500

    
        return marshal(instituicoesEnsino, instituicao_fields), 200
    
    def post(self):
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

            return marshal(nova_instituicao, instituicao_fields), 201

        except _sqlite3.Error as e:
            logger.error("Erro ao inserir")
            return ({"mensagem": f"Erro ao inserir: {str(e)}"}), 500


class InstituicaoResource(Resource):
    def get(self, id):
        logger.info("GET - Instituição")

        try:
            conn = getConnection()
            cursor = conn.cursor()

            cursor.execute(
                'SELECT regiao, codRegiao, UF, codUF, municipio, codMunicipio, entidade, codEntidade, matriculas_base FROM tb_instituicao WHERE codEntidade = ?', 
                (id,)
            )
            row = cursor.fetchone()

            cursor.close()
            conn.close()

            if row is None:
                return {"mensagem": "Instituição não encontrada"}, 404

            instituicao = InstituicaoEnsino(*row)
            return marshal(instituicao, instituicao_fields), 200

        except _sqlite3.Error:
            logger.error("Problema com banco de dados")
            return {"mensagem": "Problema com o banco de dados."}, 500
        

    def put(self, id):
        logger.info("PUT - Instituições")

        content = request.get_json()

        required_fields = [
            'regiao', 'codRegiao', 'UF', 'codUF', 'municipio',
            'codMunicipio', 'entidade', 'matriculas_base'
        ]

        if not all(field in content for field in required_fields):
            logger.error("Campos ausentes")
            return {"mensagem": "Campos ausentes"}, 400

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
                logger.error("Instituição não encontrada")
                return {"mensagem": "Instituição não encontrada"}, 404

            conn.commit()

            content['codEntidade'] = id
            return marshal(content, instituicao_fields), 200

        except _sqlite3.Error:
            logger.error("Erro ao atualizar")
            return {"mensagem": "Erro ao atualizar."}, 500
        
    def delete(self, id):
        logger.info("DELETE - Instituições")
        try:
            conn = getConnection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM tb_instituicao WHERE codEntidade = ?", (id,))

            if cursor.rowcount == 0:
                logger.error("Instituição não encontrada")
                return ({"mensagem": "Instituição não encontrada"}), 404

            conn.commit()
            resposta = {"mensagem": "Instituição removida com sucesso"}
            return marshal(resposta, instituicao_fields), 200

        except _sqlite3.Error:
            logger.error("Erro ao remover a instituição")
            return ({"mensagem": "Erro ao remover instituição."}), 500