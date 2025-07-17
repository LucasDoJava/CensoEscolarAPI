from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor 
from marshmallow import ValidationError

from helpers.application import app, api
from helpers.database import getConnection, db 
from helpers.logging import logger
from helpers.CORS import cors

from Models import UF, Mesorregiao, Microrregiao, Municipio, Instituicao


from resources.InstituicaoResource import InstituicoesResource, InstituicaoResource
from resources.indexResource import IndexResource

from Models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchemas, UFSchema, MesorregiaoSchema, MicrorregiaoSchema, MunicipioSchema


cors.init_app(app)

# Define as rotas da API
api.add_resource(IndexResource, '/')
api.add_resource(InstituicoesResource, '/instituicoes')
api.add_resource(InstituicaoResource, '/instituicoes/<int:id>')

# Configuração da conexão com PostgreSQL
DB_CONFIG = {
    'dbname': 'censoescolar',
    'user': 'postgres',
    'password': '!@LuizInacio008',
    'host': 'localhost',
    'port': 5432
}

@app.route('/instituicoess', methods=['GET'])
def get_instituicoes():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
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
                    LIMIT %s OFFSET %s;
                """, (per_page, offset))

                resultados = cursor.fetchall()

        return jsonify(resultados)
    except Exception as e:
        logger.error(f"Erro ao buscar instituições: {e}")
        return jsonify({"erro": "Erro ao buscar dados"}), 500



@app.route('/censoescolar', methods=['GET'])
def get_censo_escolar():
    ano = request.args.get('ano')
    estado = request.args.get('estado')

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT 
                        uf.nomeEstado as estado,
                        i.ano,
                        SUM(i.matriculas_base) as total_matriculas
                    FROM tb_instituicao i
                    JOIN tb_UF uf ON i.codUF = uf.codUF
                    WHERE 1=1
                """
                params = []
                
                if ano:
                    query += " AND i.ano = %s"
                    params.append(int(ano))
                
                if estado and estado != 'Todos':
                    query += " AND uf.nomeEstado = %s"
                    params.append(estado)
                
                query += " GROUP BY uf.nomeEstado, i.ano ORDER BY uf.nomeEstado"
                
                cursor.execute(query, params)
                resultados = cursor.fetchall()

        return jsonify(resultados)
    except Exception as e:
        logger.error(f"Erro ao buscar dados do censo escolar: {e}")
        return jsonify({"erro": "Erro ao buscar dados do censo escolar"}), 500


if __name__ == '__main__':
    app.run(debug=True)

    with app.app_context():
        db.create_all()
