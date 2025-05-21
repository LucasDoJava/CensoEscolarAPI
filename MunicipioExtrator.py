import pandas as pd
import requests
import json
from helpers.logging import logger


url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
resposta = requests.get(url)
dados_json = resposta.json()


df_municipios = pd.DataFrame(dados_json)


def get_nested(d, keys):
    try:
        for key in keys:
            d = d[key]
        return d
    except (TypeError, KeyError):
        return None

df_municipios["regiao"] = df_municipios["microrregiao"].apply(lambda x: get_nested(x, ["mesorregiao", "UF", "regiao", "nome"]))
df_municipios["codUF"] = df_municipios["microrregiao"].apply(lambda x: get_nested(x, ["mesorregiao", "UF", "id"]))
df_municipios["codMesorregiao"] = df_municipios["microrregiao"].apply(lambda x: get_nested(x, ["mesorregiao", "id"]))
df_municipios["codMicrorregiao"] = df_municipios["microrregiao"].apply(lambda x: get_nested(x, ["id"]))


df_nordeste = df_municipios[df_municipios["regiao"] == "Nordeste"]

df_nordeste = df_nordeste[[
    "id", "nome", "codUF", "regiao",
    "codMesorregiao", "codMicrorregiao"
]].rename(columns={
    "id": "idMunicipio",
    "nome": "nomeMunicipio"
})


json_nordeste = df_nordeste.to_json(orient="records", force_ascii=False, indent=2)


with open("municipios_nordeste.json", "w", encoding="utf-8") as f:
    f.write(json_nordeste)

logger.info("Município Add")