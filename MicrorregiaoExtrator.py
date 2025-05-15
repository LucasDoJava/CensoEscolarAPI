import requests
import json


url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"


response = requests.get(url)
response.raise_for_status()  


data = response.json()


microrregioes_nordeste = []
for item in data:
    regiao_nome = item["mesorregiao"]["UF"]["regiao"]["nome"]
    if regiao_nome == "Nordeste":
        microrregioes_nordeste.append({
            "codMicrorregiao": item["id"],
            "microrregiao": item["nome"],
            "codMesorregiao": item["mesorregiao"]["id"],
            "codUF": item["mesorregiao"]["UF"]["id"],
            "regiao": regiao_nome
        })

with open("microrregioes_nordeste.json", "w", encoding="utf-8") as f:
    json.dump(microrregioes_nordeste, f, ensure_ascii=False, indent=4)

print("microrregioes_nordeste.json salvo com sucesso!")
