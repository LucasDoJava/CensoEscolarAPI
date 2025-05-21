import requests
import pandas as pd
from helpers.logging import logger


url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"


resposta = requests.get(url)
dados_json = resposta.json()

df_mesorregioes = pd.DataFrame(dados_json)


df_mesorregioes["codUF"] = df_mesorregioes["UF"].apply(lambda x: x["id"])
df_mesorregioes["regiao"] = df_mesorregioes["UF"].apply(lambda x: x["regiao"]["nome"])



df_nordeste = df_mesorregioes[df_mesorregioes["regiao"] == "Nordeste"]


df_formatado = df_nordeste[["id", "nome", "codUF", "regiao"]].rename(columns={
    "id": "codMesorregiao",
    "nome": "mesorregiao"
})

json_nordeste = df_formatado.to_json(orient="records", force_ascii=False, indent=2)

with open("mesorregioes_nordeste.json", "w", encoding="utf-8") as f:
    f.write(json_nordeste)

logger.info("Mesorregião Add")
print("Arquivo 'mesorregioes_nordeste.json' salvo com sucesso.")
