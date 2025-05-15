import pandas as pd
import requests
import json


url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

resposta = requests.get(url)
dados_json = resposta.json()

df_estados = pd.DataFrame(dados_json)

df_estados["regiao_nome"] = df_estados["regiao"].apply(lambda x: x["nome"])
df_nordeste = df_estados[df_estados["regiao_nome"] == "Nordeste"]

df_nordeste = df_nordeste[["id", "sigla", "nome", "regiao_nome"]].rename(columns={
    "id": "codUF",
    "sigla": "UF",
    "nome": "nomeEstado",
    "regiao_nome": "região"
})

json_nordeste = df_nordeste.to_json(orient="records", force_ascii=False, indent=2)

with open("estados_nordeste.json", "w", encoding="utf-8") as f:
     f.write(json_nordeste)