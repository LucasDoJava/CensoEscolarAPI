import psycopg2
import csv
import json

# Configuração da conexão PostgreSQL
DB_CONFIG = {
    'dbname': 'censoescolar',
    'user': 'postgres',
    'password': '!@LuizInacio008',
    'host': 'localhost',
    'port': 5432
}

SCHEMA_FILE = "schemas.sql"
CSV_FILES = ["censo_escolar2023.csv", "censo_escolar2024.csv"]
JSON_ESTADOS_FILE = "estados_brasil.json"
JSON_MUNICIPIOS_FILE = "municipios_brasil.json"
JSON_MESORREGIOES_FILE = "mesorregioes_brasil.json"
JSON_MICRORREGIOES_FILE = "microrregioes_brasil.json"


for key, value in DB_CONFIG.items():
    try:
        if isinstance(value, str):
            print(f"{key}: {value} -> {value.encode('utf-8')}")
        else:
            print(f"{key}: {value} (tipo {type(value)})")
    except UnicodeEncodeError as e:
        print(f"Erro de codificação em {key}: {value}")

# Executar schema
with psycopg2.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cursor:
        with open(SCHEMA_FILE, "r", encoding="utf-8-sig") as schema_file:
            cursor.execute(schema_file.read())
        conn.commit()

# Inserir estados
with psycopg2.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cursor:
        with open(JSON_ESTADOS_FILE, "r", encoding="utf-8") as json_file:
            estados = json.load(json_file)

        for estado in estados:
            id_estado = int(estado["codUF"])
            uf = estado["UF"].strip()
            nome_estado = estado["nomeEstado"].strip()
            regiao = estado["região"].strip()

            cursor.execute("""
                INSERT INTO tb_UF (
                    codUF, UF, nomeEstado, regiao
                ) VALUES (%s, %s, %s, %s)
                ON CONFLICT (codUF) DO UPDATE SET
                    UF = EXCLUDED.UF,
                    nomeEstado = EXCLUDED.nomeEstado,
                    regiao = EXCLUDED.regiao
            """, (id_estado, uf, nome_estado, regiao))

        conn.commit()

# Inserir mesorregiões
with psycopg2.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cursor:
        with open(JSON_MESORREGIOES_FILE, "r", encoding="utf-8") as json_file:
            mesorregioes = json.load(json_file)

        for row in mesorregioes:
            codMesorregiao = int(row["codMesorregiao"])
            mesorregiao = row["mesorregiao"].strip()
            codUF = int(row["codUF"])
            regiao = row["regiao"].strip()

            cursor.execute("""
                INSERT INTO tb_Mesorregiao (
                    codMesorregiao, mesorregiao, codUF, regiao
                ) VALUES (%s, %s, %s, %s)
                ON CONFLICT (codMesorregiao) DO UPDATE SET
                    mesorregiao = EXCLUDED.mesorregiao,
                    codUF = EXCLUDED.codUF,
                    regiao = EXCLUDED.regiao
            """, (
                codMesorregiao, mesorregiao, codUF, regiao
            ))
        conn.commit()

# Inserir microrregiões
with psycopg2.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cursor:
        with open(JSON_MICRORREGIOES_FILE, "r", encoding="utf-8") as json_file:
            microrregioes = json.load(json_file)

        for row in microrregioes:
            codMicrorregiao = int(row["codMicrorregiao"])
            microrregiao = row["microrregiao"].strip()
            codMesorregiao = int(row["codMesorregiao"])
            codUF = int(row["codUF"])
            regiao = row["regiao"].strip()

            cursor.execute("""
                INSERT INTO tb_Microrregiao (
                    codMicrorregiao, microrregiao, codMesorregiao,
                    codUF, regiao
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (codMicrorregiao) DO UPDATE SET
                    microrregiao = EXCLUDED.microrregiao,
                    codMesorregiao = EXCLUDED.codMesorregiao,
                    codUF = EXCLUDED.codUF,
                    regiao = EXCLUDED.regiao
            """, (
                codMicrorregiao, microrregiao, codMesorregiao,
                codUF, regiao
            ))
        conn.commit()

# Inserir municípios 
with psycopg2.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cursor:
        with open(JSON_MUNICIPIOS_FILE, "r", encoding="utf-8") as json_file:
            municipios = json.load(json_file)

        for row in municipios:
            idMunicipio = int(row["idMunicipio"])
            nomeMunicipio = row["nomeMunicipio"].strip()
            codUF = int(row["codUF"])
            regiao = row["regiao"].strip()
            codMesorregiao = int(row["codMesorregiao"])
            codMicrorregiao = int(row["codMicrorregiao"])

            cursor.execute("""
                INSERT INTO tb_Municipio (
                    idMunicipio, nomeMunicipio, codUF,
                    regiao, codMesorregiao, codMicrorregiao
                ) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (idMunicipio) DO UPDATE SET
                    nomeMunicipio = EXCLUDED.nomeMunicipio,
                    codUF = EXCLUDED.codUF,
                    regiao = EXCLUDED.regiao,
                    codMesorregiao = EXCLUDED.codMesorregiao,
                    codMicrorregiao = EXCLUDED.codMicrorregiao
            """, (
                idMunicipio, nomeMunicipio, codUF,
                regiao, codMesorregiao, codMicrorregiao
            ))
        conn.commit()


with psycopg2.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cursor:
        for csv_file_name in CSV_FILES:
            with open(csv_file_name, "r", encoding="utf-8-sig") as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')

                for row in reader:
                    def parse_int(field):
                        value = row[field].strip()
                        return int(float(value)) if value else 0

                    codEntidade = parse_int('codEntidade')
                    entidade = row['entidade'].strip()
                    codRegiao = parse_int('codRegiao')
                    regiao = row['regiao'].strip()
                    codUF = parse_int('codUF')
                    UF = row['UF'].strip()
                    codMunicipio = parse_int('codMunicipio')
                    municipio = row['municipio'].strip()
                    matriculas_base = parse_int('matriculas_base')  
                    ano = parse_int('ano')

                    cursor.execute("""
                        INSERT INTO tb_instituicao (
                            codEntidade, entidade, codRegiao, regiao, codUF, UF,
                            codMunicipio, municipio, matriculas_base, ano
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (codEntidade, ano) DO UPDATE SET
                            entidade = EXCLUDED.entidade,
                            codRegiao = EXCLUDED.codRegiao,
                            regiao = EXCLUDED.regiao,
                            codUF = EXCLUDED.codUF,
                            UF = EXCLUDED.UF,
                            codMunicipio = EXCLUDED.codMunicipio,
                            municipio = EXCLUDED.municipio,
                            matriculas_base = EXCLUDED.matriculas_base
                    """, (
                        codEntidade, entidade, codRegiao, regiao, codUF, UF,
                        codMunicipio, municipio, matriculas_base, ano
                    ))
        conn.commit()

print("✅ Todos os dados foram inseridos com sucesso no PostgreSQL.")
