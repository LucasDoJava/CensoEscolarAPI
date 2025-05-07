class InstituicaoEnsino:
    def __init__(self, regiao, codRegiao, UF, codUF, municipio,
                 codMunicipio, mesoregiao, codMesoregiao, microregiao,
                 codMicroregiao, entidade, codEntidade, matriculas_base):
        self.regiao = regiao
        self.codRegiao = codRegiao
        self.UF = UF
        self.codUF = codUF
        self.municipio = municipio
        self.codMunicipio = codMunicipio
        self.mesoregiao = mesoregiao
        self.codMesoregiao = codMesoregiao
        self.microregiao = microregiao
        self.codMicroregiao = codMicroregiao
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
            "mesoregiao": self.mesoregiao,
            "codMesoregiao": self.codMesoregiao,
            "microregiao": self.microregiao,
            "codMicroregiao": self.codMicroregiao,
            "entidade": self.entidade,
            "codEntidade": self.codEntidade,
            "matriculas_base": self.matriculas_base
        }
