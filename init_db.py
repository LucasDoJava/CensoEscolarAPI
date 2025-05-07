import sqlite3
import csv


with sqlite3.connect('censoescolar.db') as connection:
    with open('schemas.sql', 'r', encoding='utf-8') as schema_file:
        connection.executescript(schema_file.read())


with sqlite3.connect('censoescolar.db') as connection:
    cursor = connection.cursor()

    with open('censo_escolar.csv', 'r', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')

        for row in reader:
            def parse_int(field):
                value = row[field].strip()
                return int(float(value)) if value else 0

            entidade = row['entidade'].strip()
            codRegiao = parse_int('codRegião')
            regiao = row['região'].strip()
            codUF = parse_int('codUF')
            UF = row['UF'].strip()
            codMunicipio = parse_int('codMunicípio')
            municipio = row['município'].strip()
            codMesoregiao = parse_int('codMesoregião')
            mesoregiao = row['mesoregião'].strip()
            codMicroregiao = parse_int('codMicroregião')
            microregiao = row['microregião'].strip()
            matriculas_base = parse_int('matrículas base')

            cursor.execute("""
                INSERT INTO tb_instituicao (
                    entidade, codRegiao, regiao, codUF, UF,
                    codMunicipio, municipio, codMesoregiao,
                    mesoregiao, codMicroregiao, microregiao,
                    matriculas_base
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entidade, codRegiao, regiao, codUF, UF,
                codMunicipio, municipio, codMesoregiao,
                mesoregiao, codMicroregiao, microregiao,
                matriculas_base
            ))

    connection.commit()
