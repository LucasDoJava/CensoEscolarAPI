import pandas as pd
from helpers.logging import logger

dados = pd.read_csv("microdados_ed_basica_2024.csv", encoding="ISO-8859-1", delimiter=";")

dados_filtrados = dados[dados["NO_REGIAO"] == "Nordeste"]


colunas_selecionadas = {
    "NO_REGIAO": "regiao",
    "CO_REGIAO": "codRegiao",
    "SG_UF": "UF",
    "CO_UF": "codUF",
    "NO_MUNICIPIO": "municipio",
    "CO_MUNICIPIO": "codMunicipio",
    "NO_ENTIDADE": "entidade",
    "CO_ENTIDADE": "codEntidade",
    "QT_MAT_BAS": "matrículas base"
}

dados_para_csv = dados_filtrados[list(colunas_selecionadas.keys())].rename(columns=colunas_selecionadas)

logger.info("Censo Add")
dados_para_csv.to_csv("censo_escolar.csv", index=False, encoding="utf-8-sig", sep=";")
