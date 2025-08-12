from flask_restful import Resource, marshal
from helpers.database import db
from Models.Mesorregiao import tb_Mesorregiao, tb_Mesorregiao_fields
from flask import request
from sqlalchemy.exc import IntegrityError

class MesorregioesResource(Resource):
    def get(self):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 50, type=int)
            
            mesorregioes = db.session.query(tb_Mesorregiao).paginate(
                page=page, 
                per_page=per_page,
                error_out=False
            )
            
            return {
                'data': marshal(mesorregioes.items, tb_Mesorregiao_fields),
                'total': mesorregioes.total,
                'pages': mesorregioes.pages,
                'current_page': mesorregioes.page
            }, 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar mesorregiões: {str(e)}"}, 500

    def post(self):
        dados = request.get_json()

        campos_obrigatorios = ["codmesorregiao", "mesorregiao", "coduf", "regiao"]
        for campo in campos_obrigatorios:
            if campo not in dados:
                return {"mensagem": f"Campo '{campo}' é obrigatório"}, 400

        try:
            nova_meso = tb_Mesorregiao(
                codmesorregiao=dados["codmesorregiao"],
                mesorregiao=dados["mesorregiao"],
                coduf=dados["coduf"],
                regiao=dados["regiao"]
            )
            
            db.session.add(nova_meso)
            db.session.commit()
            return marshal(nova_meso, tb_Mesorregiao_fields), 201

        except IntegrityError as e:
            db.session.rollback()
            if "duplicate key" in str(e):
                return {
                    "mensagem": "Já existe uma mesorregião com este código",
                    "codmesorregiao": dados["codmesorregiao"]
                }, 409
            return {"mensagem": f"Erro de integridade ao criar mesorregião: {str(e)}"}, 400

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao criar mesorregião: {str(e)}"}, 500


class MesorregiaoResource(Resource):
    def get(self, id):
        try:
            meso = db.session.get(tb_Mesorregiao, id)
            if not meso:
                return {
                    "mensagem": "Mesorregião não encontrada",
                    "codmesorregiao": id
                }, 404

            return marshal(meso, tb_Mesorregiao_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar mesorregião: {str(e)}"}, 500

    def put(self, id):
        try:
            meso = db.session.get(tb_Mesorregiao, id)
            if not meso:
                return {"mensagem": "Mesorregião não encontrada"}, 404

            dados = request.get_json()

            campos_permitidos = ["mesorregiao", "coduf", "regiao"]
            for campo in campos_permitidos:
                if campo in dados:
                    setattr(meso, campo, dados[campo])

            db.session.commit()
            return marshal(meso, tb_Mesorregiao_fields), 200

        except IntegrityError as e:
            db.session.rollback()
            return {"mensagem": f"Erro de integridade ao atualizar: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao atualizar mesorregião: {str(e)}"}, 500

    def delete(self, id):
        try:
            meso = db.session.get(tb_Mesorregiao, id)
            if not meso:
                return {"mensagem": "Mesorregião não encontrada"}, 404

            db.session.delete(meso)
            db.session.commit()
            return "", 204

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao remover mesorregião: {str(e)}"}, 500
