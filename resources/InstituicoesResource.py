from flask_restful import Resource, marshal
from helpers.database import db
from Models.Instituicao import tb_instituicao, tb_instituicao_fields
from Models.Municipio import tb_Municipio
from flask import request
from sqlalchemy.exc import IntegrityError

class InstituicoesResource(Resource):
    def get(self):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 50, type=int)
            
            instituicoes = db.session.query(tb_instituicao).paginate(
                page=page, 
                per_page=per_page,
                error_out=False
            )
            
            return {
                'data': marshal(instituicoes.items, tb_instituicao_fields),
                'total': instituicoes.total,
                'pages': instituicoes.pages,
                'current_page': instituicoes.page
            }, 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar instituições: {str(e)}"}, 500

    def post(self):
        dados = request.get_json()
        
        campos_obrigatorios = [
            "regiao", "codregiao", "UF", "coduf", "municipio", "codmunicipio",
            "entidade", "codentidade", "matriculas_base", "ano"
        ]
        
        for campo in campos_obrigatorios:
            if campo not in dados:
                return {"mensagem": f"Campo '{campo}' é obrigatório"}, 400

        municipio = db.session.query(tb_Municipio).get(dados["codmunicipio"])
        if not municipio:
            return {
                "mensagem": f"Município com código {dados['codmunicipio']} não encontrado",
                "sugestao": "Verifique a lista de municípios disponíveis"
            }, 400

        try:
            nova_instituicao = tb_instituicao(
                regiao=dados["regiao"],
                codregiao=dados["codregiao"],
                UF=dados["UF"],
                coduf=dados["coduf"],
                municipio=dados["municipio"],
                codmunicipio=dados["codmunicipio"],
                entidade=dados["entidade"],
                codentidade=dados["codentidade"],
                matriculas_base=dados["matriculas_base"],
                ano=dados["ano"]
            )
            
            db.session.add(nova_instituicao)
            db.session.commit()
            
            return marshal(nova_instituicao, tb_instituicao_fields), 201
        
        except IntegrityError as e:
            db.session.rollback()
            if "duplicate key" in str(e):
                return {
                    "mensagem": "Já existe uma instituição com este código",
                    "codentidade": dados["codentidade"]
                }, 409
            return {"mensagem": f"Erro de integridade ao criar instituição: {str(e)}"}, 400
            
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao criar instituição: {str(e)}"}, 500


class InstituicaoResource(Resource):
    def get(self, id):
        try:
            instituicao = db.session.query(tb_instituicao).get(id)
            if not instituicao:
                return {
                    "mensagem": "Instituição não encontrada",
                    "codentidade": id
                }, 404
                
            return marshal(instituicao, tb_instituicao_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar instituição: {str(e)}"}, 500

    def put(self, id):
        try:
            instituicao = db.session.query(tb_instituicao).get(id)
            if not instituicao:
                return {"mensagem": "Instituição não encontrada"}, 404
                
            dados = request.get_json()
            
            if 'codmunicipio' in dados:
                municipio = db.session.query(tb_Municipio).get(dados['codmunicipio'])
                if not municipio:
                    return {
                        "mensagem": f"Município com código {dados['codmunicipio']} não encontrado"
                    }, 400

            campos_permitidos = [
                "regiao", "codregiao", "UF", "coduf", "municipio",
                "codmunicipio", "entidade", "matriculas_base", "ano"
            ]
            
            for campo in campos_permitidos:
                if campo in dados:
                    setattr(instituicao, campo, dados[campo])
            
            db.session.commit()
            return marshal(instituicao, tb_instituicao_fields), 200
            
        except IntegrityError as e:
            db.session.rollback()
            return {"mensagem": f"Erro de integridade ao atualizar: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao atualizar instituição: {str(e)}"}, 500

    def delete(self, id):
        try:
            instituicao = db.session.query(tb_instituicao).get(id)
            if not instituicao:
                return {"mensagem": "Instituição não encontrada"}, 404
                
            db.session.delete(instituicao)
            db.session.commit()
            return "", 204
            
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao remover instituição: {str(e)}"}, 500