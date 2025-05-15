from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Range, Length

class InstituicaoEnsino:
    def __init__(self, regiao, codRegiao, UF, codUF, municipio,
                 codMunicipio, mesorregiao, codMesorregiao, microrregiao,
                 codMicrorregiao, entidade, codEntidade, matriculas_base):
        self.regiao = regiao
        self.codRegiao = codRegiao
        self.UF = UF
        self.codUF = codUF
        self.municipio = municipio
        self.codMunicipio = codMunicipio
        self.mesorregiao = mesorregiao
        self.codMesorregiao = codMesorregiao
        self.microrregiao = microrregiao
        self.codMicrorregiao = codMicrorregiao
        self.entidade = entidade
        self.codEntidade = codEntidade
        self.matriculas_base = matriculas_base


    def toDict(self):
        return {
            "regiao": self.regiao,
            "codRegiao": self.codRegiao,
            "UF": self.UF,
            "codUF": self.codUF,
            "municipio": self.municipio,
            "codMunicipio": self.codMunicipio,
            "mesorregiao": self.mesorregiao,
            "codMesorregiao": self.codMesorregiao,
            "microrregiao": self.microrregiao,
            "codMicrorregiao": self.codMicrorregiao,
            "entidade": self.entidade,
            "codEntidade": self.codEntidade,
            "matriculas_base": self.matriculas_base
        }

class InstituicaoEnsinoSchemas(Schema):
     regiao = fields.String(required=True, validate=Length(min=2, max=20))
     codRegiao = fields.Integer(required=True, validate=Range(min=1))
     UF = fields.String(required=True, validate=Length(equal=2))  
     codUF = fields.Integer(required=True, validate=Range(min=2))
     municipio = fields.String(required=True, validate=Length(min=2, max=150))
     codMunicipio = fields.Integer(required=True, validate=Range(min=7))
     mesorregiao = fields.String(required=True, validate=Length(min=2, max=100))
     codMesorregiao = fields.Integer(required=True, validate=Range(min=4))
     microrregiao = fields.String(required=True, validate=Length(min=2, max=100))
     codMicrorregiao = fields.Integer(required=True, validate=Range(min=5))
     entidade = fields.String(required=True, validate=Length(min=2, max=100))
     codEntidade = fields.Integer(required=True, validate=Range(min=1))
     matriculas_base = fields.Integer(required=True, validate=Range(min=0))

class UF:
    def __init__(self, codUF, UF, nomeUF, regiao):
        self.codUF = codUF
        self.UF = UF
        self.nomeUF = nomeUF
        self.regiao = regiao

class UFSchema(Schema):
    codUF = fields.Integer()
    UF = fields.String(required=True, validate=Length(min=2, max=100))
    nomeUF = fields.String(required=True, validate=Length(min=2, max=100))
    regiao = fields.String(required=True, validate=Length(min=2, max=100))

class Municipio:
    def __init__(self, codMunicipio, nomeMunicipio, codUF, regiao, codMesorregiao, codMicrorregiao):
        self.codMunicipio = codMunicipio
        self.nomeMunicipio = nomeMunicipio
        self.codUF = codUF
        self.regiao = regiao
        self.codMesorregiao = codMesorregiao
        self.codMicrorregiao = codMicrorregiao

class MunicipioSchema(Schema):
    codMunicipio = fields.Integer()
    nomeMunicipio = fields.String(required=True, validate=Length(min=2, max=100))
    codUF = fields.Integer()
    regiao = fields.String(required=True, validate=Length(min=2, max=100))
    codMesorregiao = fields.Integer()
    codMicrorregiao = fields.Integer()

class Mesorregiao:
    def __init__(self, codMesorregiao, mesorregiao, codUF, regiao):
        self.codMesorregiao = codMesorregiao
        self.mesorregiao = mesorregiao
        self.codUF = codUF
        self.regiao = regiao

class MesorregiaoSchema(Schema):
    codMesorregiao = fields.Integer()
    mesorregiao = fields.String(required=True, validate=Length(min=2, max=100))
    codUF = fields.Integer()
    regiao = fields.String(required=True, validate=Length(min=2, max=100))

class Microrregiao:
    def __init__(self, codMicrorregiao, microrregiao, codMesorregiao, codUF, regiao):
        self.codMicrorregiao = codMicrorregiao
        self.microrregiao = microrregiao
        self.codMesorregiao = codMesorregiao
        self.codUF = codUF
        self.regiao = regiao

class MicrorregiaoSchema(Schema):
    codMicrorregiao = fields.Integer()
    microrregiao = fields.String(required=True, validate=Length(min=2, max=100))
    codMesorregiao = fields.Integer()
    codUF = fields.Integer()
    regiao = fields.String(required=True, validate=Length(min=2, max=100))