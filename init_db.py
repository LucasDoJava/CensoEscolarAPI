import json
import psycopg2
import csv

DB_CONFIG = {
    'dbname': 'censoescolar',
    'user': 'postgres',
    'password': '!@LuizInacio008',
    'host': 'localhost',
    'port': 5432
}

# Caminhos dos arquivos JSON
JSON_ESTADOS_FILE = "estados_brasil.json"
JSON_MESORREGIOES_FILE = "mesorregioes_brasil.json"
JSON_MICRORREGIOES_FILE = "microrregioes_brasil.json"
JSON_MUNICIPIOS_FILE = "municipios_brasil.json"
CSV_FILES = ["censo_escolar2023.csv", "censo_escolar2024.csv"]

with psycopg2.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cursor:

        # UF
        with open(JSON_ESTADOS_FILE, "r", encoding="utf-8") as file:
            estados = json.load(file)
        for uf in estados:
            cursor.execute("""
                INSERT INTO "tb_UF" (coduf, uf, nomeestado, regiao)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (coduf) DO UPDATE SET
                    uf = EXCLUDED.uf,
                    nomeestado = EXCLUDED.nomeestado,
                    regiao = EXCLUDED.regiao
            """, (int(uf["codUF"]), uf["UF"].strip(), uf["nomeEstado"].strip(), uf["região"].strip()))

        # Mesorregião
        with open(JSON_MESORREGIOES_FILE, "r", encoding="utf-8") as file:
            mesorregioes = json.load(file)
        for meso in mesorregioes:
            cursor.execute("""
                INSERT INTO "tb_Mesorregiao" (codmesorregiao, mesorregiao, coduf, regiao)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (codmesorregiao) DO UPDATE SET
                    mesorregiao = EXCLUDED.mesorregiao,
                    coduf = EXCLUDED.coduf,
                    regiao = EXCLUDED.regiao
            """, (int(meso["codMesorregiao"]), meso["mesorregiao"].strip(), int(meso["codUF"]), meso["regiao"].strip()))

        # Microrregião
        with open(JSON_MICRORREGIOES_FILE, "r", encoding="utf-8") as file:
            microrregioes = json.load(file)
        for micro in microrregioes:
            cursor.execute("""
                INSERT INTO "tb_Microrregiao" (codmicrorregiao, microrregiao, codmesorregiao, coduf, regiao)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (codmicrorregiao) DO UPDATE SET
                    microrregiao = EXCLUDED.microrregiao,
                    codmesorregiao = EXCLUDED.codmesorregiao,
                    coduf = EXCLUDED.coduf,
                    regiao = EXCLUDED.regiao
            """, (
                int(micro["codMicrorregiao"]), micro["microrregiao"].strip(), int(micro["codMesorregiao"]),
                int(micro["codUF"]), micro["regiao"].strip()
            ))

        # Município
        with open(JSON_MUNICIPIOS_FILE, "r", encoding="utf-8") as file:
            municipios = json.load(file)
        for municipio in municipios:
            cursor.execute("""
                INSERT INTO "tb_Municipio" (idmunicipio, nomemunicipio, coduf, regiao, codmesorregiao, codmicrorregiao)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (idmunicipio) DO UPDATE SET
                    nomemunicipio = EXCLUDED.nomemunicipio,
                    coduf = EXCLUDED.coduf,
                    regiao = EXCLUDED.regiao,
                    codmesorregiao = EXCLUDED.codmesorregiao,
                    codmicrorregiao = EXCLUDED.codmicrorregiao
            """, (
                int(municipio["idMunicipio"]), municipio["nomeMunicipio"].strip(), int(municipio["codUF"]),
                municipio["regiao"].strip(), int(municipio["codMesorregiao"]), int(municipio["codMicrorregiao"])
            ))

        # Instituição
def normalize_key(key: str) -> str:
    
    return key.strip().lower()

with psycopg2.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cursor:
        for csv_file_name in CSV_FILES:
            with open(csv_file_name, "r", encoding="utf-8-sig") as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')

                
                normalized_keys = {normalize_key(k): k for k in reader.fieldnames}

                for row in reader:
                    
                    def get_value(field_normalized):
                        key_original = normalized_keys.get(field_normalized)
                        if key_original is None:
                            raise KeyError(f"Campo '{field_normalized}' não encontrado no CSV")
                        return row[key_original].strip()

                    try:
                        codentidade = int(float(get_value('codentidade')))
                        entidade = get_value('entidade')
                        codregiao = int(float(get_value('codregiao')))
                        regiao = get_value('regiao')
                        coduf = int(float(get_value('coduf')))
                        uf = get_value('uf')
                        codmunicipio = int(float(get_value('codmunicipio')))
                        municipio = get_value('municipio')
                        matriculas_base_str = get_value('matriculas_base').replace('.', '')  # tira ponto se tiver
                        matriculas_base = int(matriculas_base_str) if matriculas_base_str else 0
                        ano = int(float(get_value('ano')))

                        cursor.execute("""
                            INSERT INTO tb_instituicao (
                                codentidade, entidade, codregiao, regiao, coduf, uf,
                                codmunicipio, municipio, matriculas_base, ano, created
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                            ON CONFLICT (codentidade, ano) DO UPDATE SET
                                entidade = EXCLUDED.entidade,
                                codregiao = EXCLUDED.codregiao,
                                regiao = EXCLUDED.regiao,
                                coduf = EXCLUDED.coduf,
                                uf = EXCLUDED.uf,
                                codmunicipio = EXCLUDED.codmunicipio,
                                municipio = EXCLUDED.municipio,
                                matriculas_base = EXCLUDED.matriculas_base,
                                ano = EXCLUDED.ano
                        """, (
                            codentidade, entidade, codregiao, regiao, coduf, uf,
                            codmunicipio, municipio, matriculas_base, ano
                        ))

                    except Exception as e:
                        print(f"Erro ao inserir linha com codentidade {row.get('codentidade', 'desconhecido')}: {e}")

        conn.commit()

print("✅ Dados das instituições inseridos com sucesso!")
