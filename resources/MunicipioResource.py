from flask_restful import Resource, marshal
from helpers.database import db
from Models.Municipio import tb_Municipio, tb_Municipio_fields
from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class MunicipiosResource(Resource):
    def get(self):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 50, type=int)

            municipios = db.session.query(tb_Municipio).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

            return {
                'data': marshal(municipios.items, tb_Municipio_fields),
                'total': municipios.total,
                'pages': municipios.pages,
                'current_page': municipios.page
            }, 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar municípios: {str(e)}"}, 500

    def post(self):
        try:
            dados = request.get_json()

            campos_obrigatorios = [
                "idmunicipio", "nome_municipio", "coduf",
                "regiao", "codmesorregiao", "codmicrorregiao"
            ]
            for campo in campos_obrigatorios:
                if campo not in dados:
                    return {"mensagem": f"Campo '{campo}' é obrigatório"}, 400

            novo_municipio = tb_Municipio(
                idmunicipio=dados["idmunicipio"],
                nome_municipio=dados["nome_municipio"],
                coduf=dados["coduf"],
                regiao=dados["regiao"],
                codmesorregiao=dados["codmesorregiao"],
                codmicrorregiao=dados["codmicrorregiao"]
            )

            db.session.add(novo_municipio)
            db.session.commit()

            return marshal(novo_municipio, tb_Municipio_fields), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"mensagem": f"Erro de integridade ao criar município: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao criar município: {str(e)}"}, 500


class MunicipioResource(Resource):
    def get(self, id):
        try:
            municipio = tb_Municipio.query.get(id)
            if not municipio:
                return {"mensagem": "Município não encontrado", "idmunicipio": id}, 404
            return marshal(municipio, tb_Municipio_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar município: {str(e)}"}, 500

    def put(self, id):
        try:
            municipio = tb_Municipio.query.get(id)
            if not municipio:
                return {"mensagem": "Município não encontrado"}, 404

            dados = request.get_json()
            campos_permitidos = [
                "nome_municipio", "coduf", "regiao",
                "codmesorregiao", "codmicrorregiao"
            ]

            for campo in campos_permitidos:
                if campo in dados:
                    setattr(municipio, campo, dados[campo])

            db.session.commit()
            return marshal(municipio, tb_Municipio_fields), 200

        except IntegrityError as e:
            db.session.rollback()
            return {"mensagem": f"Erro de integridade ao atualizar município: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao atualizar município: {str(e)}"}, 500

    def delete(self, id):
        try:
            municipio = tb_Municipio.query.get(id)
            if not municipio:
                return {"mensagem": "Município não encontrado"}, 404

            db.session.delete(municipio)
            db.session.commit()
            return {"mensagem": "Município excluído com sucesso"}, 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao excluir município: {str(e)}"}, 500
