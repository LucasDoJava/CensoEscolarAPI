from flask_restful import Resource, marshal
from helpers.database import db
from Models.Microrregiao import tb_Microrregiao, tb_Microrregiao_fields
from Models.Mesorregiao import tb_Mesorregiao
from flask import request
from sqlalchemy.exc import IntegrityError

def get_next_codmicrorregiao():
    max_id = db.session.query(db.func.max(tb_Microrregiao.codmicrorregiao)).scalar()
    return (max_id or 0) + 1

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
        dados = request.get_json()

        campos_obrigatorios = ["microrregiao", "codmesorregiao", "coduf", "regiao"]
        for campo in campos_obrigatorios:
            if campo not in dados:
                return {"mensagem": f"Campo '{campo}' é obrigatório"}, 400

        mesorregiao = db.session.query(tb_Mesorregiao).get(dados["codmesorregiao"])
        if not mesorregiao:
            return {
                "mensagem": f"Mesorregião com código {dados['codmesorregiao']} não encontrada",
                "sugestao": "Verifique a lista de mesorregiões disponíveis"
            }, 400

        try:
            novo_id = get_next_codmicrorregiao()
            nova_microrregiao = tb_Microrregiao(
                codmicrorregiao=novo_id,
                microrregiao=dados["microrregiao"],
                codmesorregiao=dados["codmesorregiao"],
                coduf=dados["coduf"],
                regiao=dados["regiao"]
            )

            db.session.add(nova_microrregiao)
            db.session.commit()

            return marshal(nova_microrregiao, tb_Microrregiao_fields), 201

        except IntegrityError as e:
            db.session.rollback()
            if "duplicate key" in str(e):
                return {
                    "mensagem": "Já existe uma microrregião com este código",
                    "microrregiao": dados["microrregiao"]
                }, 409
            return {"mensagem": f"Erro de integridade ao criar microrregião: {str(e)}"}, 400

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao criar microrregião: {str(e)}"}, 500


class MicrorregiaoResource(Resource):
    def get(self, id):
        try:
            microrregiao = db.session.get(tb_Microrregiao, id)
            if not microrregiao:
                return {"mensagem": "Microrregião não encontrada"}, 404
            return marshal(microrregiao, tb_Microrregiao_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar microrregião: {str(e)}"}, 500
     
    def put(self, id):
        try:
            microrregiao = db.session.get(tb_Microrregiao, id)
            if not microrregiao:
                return {"mensagem": "Microrregião não encontrada"}, 404

            dados = request.get_json()

            if 'codmesorregiao' in dados:
                mesorregiao = db.session.query(tb_Mesorregiao).get(dados['codmesorregiao'])
                if not mesorregiao:
                    return {
                        "mensagem": f"Mesorregião com código {dados['codmesorregiao']} não encontrada"
                    }, 400

            campos_permitidos = ["microrregiao", "codmesorregiao", "coduf", "regiao"]

            for campo in campos_permitidos:
                if campo in dados:
                    setattr(microrregiao, campo, dados[campo])

            db.session.commit()
            return marshal(microrregiao, tb_Microrregiao_fields), 200

        except IntegrityError as e:
            db.session.rollback()
            return {"mensagem": f"Erro de integridade ao atualizar: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao atualizar microrregião: {str(e)}"}, 500
        
    def delete(self, id):
        try:
            microrregiao = db.session.get(tb_Microrregiao, id)
            if not microrregiao:
                return {"mensagem": "Microrregião não encontrada"}, 404

            db.session.delete(microrregiao)
            db.session.commit()
            return "", 204

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao excluir microrregião: {str(e)}"}, 500
