import sqlite3
import csv
import json

DB_FILE = "censoescolar.db"
SCHEMA_FILE = "schemas.sql"
CSV_FILE = "censo_escolar.csv"
JSON_ESTADOS_FILE = "estados_nordeste.json"
JSON_MUNICIPIOS_FILE = "municipios_nordeste.json"


with sqlite3.connect(DB_FILE) as connection:
    with open(SCHEMA_FILE, "r", encoding="utf-8") as schema_file:
        connection.executescript(schema_file.read())

with sqlite3.connect(DB_FILE) as connection:
    cursor = connection.cursor()

    with open(CSV_FILE, "r", encoding="utf-8-sig") as csv_file:
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
            matriculas_base = parse_int('matrículas base')

            cursor.execute("""
                INSERT INTO tb_instituicao (
                     codEntidade, entidade, codRegiao, regiao, codUF, UF,
                    codMunicipio, municipio, matriculas_base
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                 codEntidade, entidade, codRegiao, regiao, codUF, UF,
                codMunicipio, municipio, matriculas_base
            ))

    connection.commit()


with sqlite3.connect(DB_FILE) as connection:
    cursor = connection.cursor()

    with open(JSON_ESTADOS_FILE, "r", encoding="utf-8") as json_file:
        estados = json.load(json_file)

    for estado in estados:
        id_estado = int(estado["codUF"])
        uf = estado["UF"].strip()
        nome_estado = estado["nomeEstado"].strip()
        regiao = estado["região"].strip()

        cursor.execute("""
            INSERT OR REPLACE INTO tb_UF (
                codUF, UF, nomeEstado, regiao
            ) VALUES (?, ?, ?, ?)
        """, (id_estado, uf, nome_estado, regiao))

    connection.commit()


with sqlite3.connect(DB_FILE) as connection:
    cursor = connection.cursor()

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
            INSERT OR REPLACE INTO tb_Municipio (
                idMunicipio, nomeMunicipio, codUF,
                regiao, codMesorregiao,
                codMicrorregiao
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            idMunicipio, nomeMunicipio, codUF,
            regiao, codMesorregiao,
            codMicrorregiao
        ))

    connection.commit()

    JSON_MESORREGIOES_FILE = "mesorregioes_nordeste.json"


with sqlite3.connect(DB_FILE) as connection:
    cursor = connection.cursor()

    with open(JSON_MESORREGIOES_FILE, "r", encoding="utf-8") as json_file:
        mesorregioes = json.load(json_file)

    for row in mesorregioes:
        codMesorregiao = int(row["codMesorregiao"])
        mesorregiao = row["mesorregiao"].strip()
        codUF = int(row["codUF"])
        regiao = row["regiao"].strip()

        cursor.execute("""
            INSERT OR REPLACE INTO tb_Mesorregiao (
                codMesorregiao, mesorregiao, codUF, regiao
            ) VALUES (?, ?, ?, ?)
        """, (
            codMesorregiao, mesorregiao, codUF, regiao
        ))

    connection.commit()

JSON_MICRORREGIOES_FILE = "microrregioes_nordeste.json"

with sqlite3.connect(DB_FILE) as connection:
    cursor = connection.cursor()

    with open(JSON_MICRORREGIOES_FILE, "r", encoding="utf-8") as json_file:
        microrregioes = json.load(json_file)

    for row in microrregioes:
        codMicrorregiao = int(row["codMicrorregiao"])
        microrregiao = row["microrregiao"].strip()
        codMesorregiao = int(row["codMesorregiao"])
        codUF = int(row["codUF"])
        regiao = row["regiao"].strip()

        cursor.execute("""
            INSERT OR REPLACE INTO tb_Microrregiao (
                codMicrorregiao, microrregiao, codMesorregiao,
                codUF, regiao
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            codMicrorregiao, microrregiao, codMesorregiao,
            codUF, regiao
        ))

    connection.commit()

print("Todos os dados foram inseridos com sucesso.")
