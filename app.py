from os import read
from flask import Flask, jsonify, request, g
import _sqlite3
from marshmallow import ValidationError

from helpers.application import app, api
from helpers.database import getConnection
from helpers.logging import logger
from helpers.CORS import cors

from resources.InstituicaoResource import InstituicoesResource, InstituicaoResource
from resources.indexResource import IndexResource

from Models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchemas, UFSchema, MesorregiaoSchema, MicrorregiaoSchema, MunicipioSchema

cors.init_app(app)

api.add_resource(IndexResource, '/')
api.add_resource(InstituicoesResource, '/instituicoes')
api.add_resource(InstituicaoResource, '/instituicoes/<int:id>')
    
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
