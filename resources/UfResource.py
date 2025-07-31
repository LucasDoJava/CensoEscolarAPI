from flask_restful import Resource, marshal
from helpers.database import db
from Models.UF import tb_UF, tb_UF_fields
from flask import request
from sqlalchemy.exc import IntegrityError

class UfsResource(Resource):
    def get(self, coduf=None):
        if coduf:
            uf = tb_UF.query.get(coduf)
            if uf:
                return marshal(uf, tb_UF_fields)
            return {"mensagem": "UF não encontrada."}, 404
        else:
            ufs = tb_UF.query.all()
            return [marshal(uf, tb_UF_fields) for uf in ufs]
        
    def post(self):
        dados = request.json
        coduf = dados.get("coduf")
        if tb_UF.query.get(coduf):
            return {"mensagem": "UF com esse código já existe."}, 409

        nova_uf = tb_UF(
            coduf=coduf,
            uf=dados["uf"],
            nome_estado=dados["nome_estado"],
            regiao=dados["regiao"]
        )
        db.session.add(nova_uf)
        db.session.commit()
        return marshal(nova_uf, tb_UF_fields), 201


class UfResource(Resource):
     def get(self, id):
        uf = tb_UF.query.get(id)
        if uf:
            return marshal(uf, tb_UF_fields), 200
        return {"mensagem": "UF não encontrada"}, 404
     
     def put(self, id):
        uf = tb_UF.query.get(id)
        if not uf:
            return {"mensagem": "UF não encontrada."}, 404

        dados = request.json
        uf.uf = dados.get("uf", uf.uf)
        uf.nome_estado = dados.get("nome_estado", uf.nome_estado)
        uf.regiao = dados.get("regiao", uf.regiao)

        db.session.commit()
        return marshal(uf, tb_UF_fields)
     
     def delete(self, id):
        uf = tb_UF.query.get(id)
        if not uf:
            return {"mensagem": "UF não encontrada."}, 404

        db.session.delete(uf)
        db.session.commit()
        return {"mensagem": "UF deletada com sucesso."}