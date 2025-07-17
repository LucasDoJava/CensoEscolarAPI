from flask import jsonify, request
from flask_restful import Resource, marshal
from marshmallow import ValidationError
import psycopg2
from psycopg2 import Error

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

            cursor.execute('SELECT * FROM tb_instituicao LIMIT %s OFFSET %s', (per_page, offset))
            resultSet = cursor.fetchall()

            for row in resultSet:
                instituicaoEnsino = InstituicaoEnsino(*row)
                instituicoesEnsino.append(instituicaoEnsino)

            cursor.close()
            conn.close()

        except Error as e:
            logger.error(f"Problema com banco: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500

        return marshal(instituicoesEnsino, instituicao_fields), 200

    def post(self):
        logger.info("POST - Instituições")
        content = request.get_json()

        required_fields = [
            'regiao', 'codRegiao', 'UF', 'codUF', 'municipio', 'codMunicipio',
            'entidade', 'codEntidade', 'matriculas_base', 'ano'
        ]

        if not all(field in content for field in required_fields):
            return jsonify({"mensagem": "Campos ausentes"}), 400

        try:
            conn = getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO tb_instituicao (
                    regiao, codRegiao, UF, codUF, municipio, codMunicipio,
                    entidade, codEntidade, matriculas_base, ano
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                content['regiao'], content['codRegiao'], content['UF'], content['codUF'],
                content['municipio'], content['codMunicipio'],
                content['entidade'], content['codEntidade'],content['matriculas_base'], content['ano']
            ))

            
            conn.commit()

            nova_instituicao = InstituicaoEnsino(
                content['regiao'], content['codRegiao'], content['UF'], content['codUF'],
                content['municipio'], content['codMunicipio'],
                content['entidade'], content['codEntidade'], content['matriculas_base'], content['ano']
            )

            return marshal(nova_instituicao, instituicao_fields), 201

        except Error as e:
            logger.error(f"Erro ao inserir: {e}")
            return {"mensagem": f"Erro ao inserir: {str(e)}"}, 500


class InstituicaoResource(Resource):
    def get(self, id):
        logger.info("GET - Instituição")

        try:
            conn = getConnection()
            cursor = conn.cursor()

            cursor.execute(
                'SELECT regiao, codRegiao, UF, codUF, municipio, codMunicipio, entidade, codEntidade, matriculas_base, ano '
                'FROM tb_instituicao WHERE codEntidade = %s',
                (id,)
            )
            row = cursor.fetchone()

            cursor.close()
            conn.close()

            if row is None:
                return {"mensagem": "Instituição não encontrada"}, 404

            instituicao = InstituicaoEnsino(*row)
            return marshal(instituicao, instituicao_fields), 200

        except Error as e:
            logger.error(f"Problema com banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500

    def put(self, id):
        logger.info("PUT - Instituições")
        content = request.get_json()

        required_fields = [
            'regiao', 'codRegiao', 'UF', 'codUF', 'municipio',
            'codMunicipio', 'entidade', 'codEntidade', 'matriculas_base', 'ano'
        ]

        if not all(field in content for field in required_fields):
            logger.error("Campos ausentes")
            return {"mensagem": "Campos ausentes"}, 400

        try:
            conn = getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE tb_instituicao SET
                    regiao = %s, codRegiao = %s, UF = %s, codUF = %s, municipio = %s,
                    codMunicipio = %s, entidade = %s, codEntidade = %s, matriculas_base = %s, ano = %s
                WHERE codEntidade = %s
            """, (
                content['regiao'], content['codRegiao'], content['UF'], content['codUF'],
                content['municipio'], content['codMunicipio'],
                content['entidade'], content['codEntidade'] ,content['matriculas_base'], content['ano'], id
            ))

            if cursor.rowcount == 0:
                logger.error("Instituição não encontrada")
                return {"mensagem": "Instituição não encontrada"}, 404

            conn.commit()
            content['codEntidade'] = id
            return marshal(content, instituicao_fields), 200

        except Error as e:
            logger.error(f"Erro ao atualizar: {e}")
            return {"mensagem": "Erro ao atualizar."}, 500

    def delete(self, id):
        logger.info("DELETE - Instituições")
        try:
            conn = getConnection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM tb_instituicao WHERE codEntidade = %s", (id,))

            if cursor.rowcount == 0:
                logger.error("Instituição não encontrada")
                return {"mensagem": "Instituição não encontrada"}, 404

            conn.commit()
            return {"mensagem": "Instituição removida com sucesso"}, 200

        except Error as e:
            logger.error(f"Erro ao remover a instituição: {e}")
            return {"mensagem": "Erro ao remover instituição."}, 500
