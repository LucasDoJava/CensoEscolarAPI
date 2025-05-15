DROP TABLE IF EXISTS tb_instituicao;

CREATE TABLE tb_instituicao (
   regiao TEXT,
    codRegiao INTEGER,
    UF TEXT,
    codUF INTEGER,
    municipio TEXT,
    codMunicipio INTEGER,
    mesorregiao TEXT,
    codMesorregiao INTEGER,
    microrregiao TEXT,
    codMicrorregiao INTEGER,
    entidade TEXT,
    codEntidade INTEGER PRIMARY KEY AUTOINCREMENT,
    matriculas_base INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tb_UF (
    codUF INTEGER PRIMARY KEY,
    UF TEXT,
    nomeEstado TEXT,
    regiao TEXT
);

CREATE TABLE IF NOT EXISTS tb_Municipio (
    idMunicipio INTEGER PRIMARY KEY,
    nomeMunicipio TEXT,
    codUF INTEGER,
   regiao TEXT,
   codMesorregiao INTEGER,
   codMicrorregiao INTEGER,
    Foreign KEY (codUF) References tb_UF,
    Foreign KEY (codMesorregiao) References tb_Mesorregiao,
    Foreign KEY (codMicrorregiao) References tb_Microrregiao
);

CREATE TABLE IF NOT EXISTS tb_Mesorregiao (
   codMesorregiao INTEGER PRIMARY KEY,
    mesorregiao TEXT,
    codUF INTEGER,
   regiao TEXT,
   Foreign KEY (codUF) References tb_UF
);

CREATE TABLE IF NOT EXISTS tb_Microrregiao (
   codMicrorregiao INTEGER PRIMARY KEY,
   microrregiao TEXT,
   codMesorregiao INTEGER,
   codUF INTEGER,
   regiao TEXT,
   Foreign KEY (codUF) References tb_UF
);
