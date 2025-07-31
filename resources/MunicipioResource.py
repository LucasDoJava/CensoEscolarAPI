from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from Models.Municipio import tb_Municipio, tb_Municipio_fields
from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class MunicipiosResource(Resource):
    def get(self):
        municipios = tb_Municipio.query.all()
        return marshal(municipios, tb_Municipio_fields), 200
    
    def post(self):
        dados = request.get_json()

        municipio = tb_Municipio(
            idmunicipio=dados["idmunicipio"],
            nome_municipio=dados["nome_municipio"],
            coduf=dados["coduf"],
            regiao=dados["regiao"],
            codmesorregiao=dados["codmesorregiao"],
            codmicrorregiao=dados["codmicrorregiao"]
        )

        db.session.add(municipio)
        db.session.commit()
        return marshal(municipio, tb_Municipio_fields), 201

class MunicipioResource(Resource):
     def get(self, id):
        municipio = tb_Municipio.query.get(id)
        if municipio:
            return marshal(municipio, tb_Municipio_fields), 200
        return {"mensagem": "Município não encontrado"}, 404
     
     def put(self, id):
        municipio = tb_Municipio.query.get(id)
        if not municipio:
            return {"mensagem": "Município não encontrado"}, 404

        dados = request.get_json()
        municipio.nome_municipio = dados.get("nome_municipio", municipio.nome_municipio)
        municipio.coduf = dados.get("coduf", municipio.coduf)
        municipio.regiao = dados.get("regiao", municipio.regiao)
        municipio.codmesorregiao = dados.get("codmesorregiao", municipio.codmesorregiao)
        municipio.codmicrorregiao = dados.get("codmicrorregiao", municipio.codmicrorregiao)

        db.session.commit()
        return marshal(municipio, tb_Municipio_fields), 200
     
     def delete(self, id):
        municipio = tb_Municipio.query.get(id)
        if not municipio:
            return {"mensagem": "Município não encontrado"}, 404

        db.session.delete(municipio)
        db.session.commit()
        return {"mensagem": "Município deletado com sucesso"}, 200