from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from Models.Microrregiao import tb_Microrregiao, tb_Microrregiao_fields
from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class MicrorregioesResource(Resource):
    def get(self):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 50, type=int)
            
            microrregioes = db.session.query(tb_Microrregiao).paginate(
                page=page, 
                per_page=per_page,
                error_out=False
            )
            
            return {
                'data': marshal(microrregioes.items, tb_Microrregiao_fields),
                'total': microrregioes.total,
                'pages': microrregioes.pages,
                'current_page': microrregioes.page
            }, 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar microrregiões: {str(e)}"}, 500
        
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("microrregiao", type=str, required=True)
        parser.add_argument("codmesorregiao", type=int, required=True)
        parser.add_argument("coduf", type=int, required=True)
        parser.add_argument("regiao", type=str, required=True)
        dados = parser.parse_args()

        nova = tb_Microrregiao(**dados)
        try:
            db.session.add(nova)
            db.session.commit()
            return marshal(nova, tb_Microrregiao_fields), 201
        except IntegrityError:
            db.session.rollback()
            return {"mensagem": "Microrregião com esse código já existe."}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao adicionar microrregião: {str(e)}"}, 500


class MicrorregiaoResource(Resource):
     def get(self, id):
        microrregiao = tb_Microrregiao.query.get(id)
        if microrregiao:
            return marshal(microrregiao, tb_Microrregiao_fields), 200
        return {"mensagem": "Microrregião não encontrada"}, 404
     
     def put(self, id):
        microrregiao = tb_Microrregiao.query.get(id)
        if not microrregiao:
            return {"mensagem": "Microrregião não encontrada"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("microrregiao", type=str)
        parser.add_argument("codmesorregiao", type=int)
        parser.add_argument("coduf", type=int)
        parser.add_argument("regiao", type=str)
        dados = parser.parse_args()

        for key, value in dados.items():
            if value is not None:
                setattr(microrregiao, key, value)
        
        try:
            db.session.commit()
            return marshal(microrregiao, tb_Microrregiao_fields), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao atualizar microrregião: {str(e)}"}, 500
        
     def delete(self, id):
        microrregiao = tb_Microrregiao.query.get(id)
        if not microrregiao:
            return {"mensagem": "Microrregião não encontrada"}, 404
        try:
            db.session.delete(microrregiao)
            db.session.commit()
            return {"mensagem": "Microrregião excluída com sucesso"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao excluir microrregião: {str(e)}"}, 500