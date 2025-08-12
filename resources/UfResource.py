from flask_restful import Resource, marshal
from helpers.database import db
from Models.UF import tb_UF, tb_UF_fields
from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class UfsResource(Resource):
    def get(self):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 50, type=int)

            ufs = db.session.query(tb_UF).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

            return {
                'data': marshal(ufs.items, tb_UF_fields),
                'total': ufs.total,
                'pages': ufs.pages,
                'current_page': ufs.page
            }, 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar UFs: {str(e)}"}, 500

    def post(self):
        try:
            dados = request.get_json()

            campos_obrigatorios = ["coduf", "uf", "nome_estado", "regiao"]
            for campo in campos_obrigatorios:
                if campo not in dados:
                    return {"mensagem": f"Campo '{campo}' é obrigatório"}, 400

            if tb_UF.query.get(dados["coduf"]):
                return {"mensagem": "UF com esse código já existe."}, 409

            nova_uf = tb_UF(
                coduf=dados["coduf"],
                uf=dados["uf"],
                nome_estado=dados["nome_estado"],
                regiao=dados["regiao"]
            )

            db.session.add(nova_uf)
            db.session.commit()
            return marshal(nova_uf, tb_UF_fields), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"mensagem": f"Erro de integridade ao criar UF: {str(e)}"}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"mensagem": f"Erro no banco de dados ao criar UF: {str(e)}"}, 500
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro inesperado ao criar UF: {str(e)}"}, 500


class UfResource(Resource):
    def get(self, id):
        try:
            uf = tb_UF.query.get(id)
            if not uf:
                return {"mensagem": "UF não encontrada", "coduf": id}, 404
            return marshal(uf, tb_UF_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar UF: {str(e)}"}, 500

    def put(self, id):
        try:
            uf = tb_UF.query.get(id)
            if not uf:
                return {"mensagem": "UF não encontrada"}, 404

            dados = request.get_json()
            campos_permitidos = ["uf", "nome_estado", "regiao"]

            for campo in campos_permitidos:
                if campo in dados:
                    setattr(uf, campo, dados[campo])

            db.session.commit()
            return marshal(uf, tb_UF_fields), 200

        except IntegrityError as e:
            db.session.rollback()
            return {"mensagem": f"Erro de integridade ao atualizar UF: {str(e)}"}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"mensagem": f"Erro no banco de dados ao atualizar UF: {str(e)}"}, 500
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro inesperado ao atualizar UF: {str(e)}"}, 500

    def delete(self, id):
        try:
            uf = tb_UF.query.get(id)
            if not uf:
                return {"mensagem": "UF não encontrada"}, 404

            db.session.delete(uf)
            db.session.commit()
            return {"mensagem": "UF excluída com sucesso"}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"mensagem": f"Erro no banco de dados ao excluir UF: {str(e)}"}, 500
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro inesperado ao excluir UF: {str(e)}"}, 500
