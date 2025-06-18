DROP TABLE IF EXISTS tb_instituicao CASCADE;
DROP TABLE IF EXISTS tb_UF CASCADE;
DROP TABLE IF EXISTS tb_Municipio CASCADE;
DROP TABLE IF EXISTS tb_Mesorregiao CASCADE;
DROP TABLE IF EXISTS tb_Microrregiao CASCADE;

CREATE TABLE tb_UF (
    codUF INTEGER PRIMARY KEY,
    UF TEXT,
    nomeEstado TEXT,
    regiao TEXT
);

CREATE TABLE tb_Mesorregiao (
    codMesorregiao INTEGER PRIMARY KEY,
    mesorregiao TEXT,
    codUF INTEGER,
    regiao TEXT,
    FOREIGN KEY (codUF) REFERENCES tb_UF (codUF)
);

CREATE TABLE tb_Microrregiao (
    codMicrorregiao INTEGER PRIMARY KEY,
    microrregiao TEXT,
    codMesorregiao INTEGER,
    codUF INTEGER,
    regiao TEXT,
    FOREIGN KEY (codUF) REFERENCES tb_UF (codUF),
    FOREIGN KEY (codMesorregiao) REFERENCES tb_Mesorregiao (codMesorregiao)
);

CREATE TABLE tb_Municipio (
    idMunicipio INTEGER PRIMARY KEY,
    nomeMunicipio TEXT,
    codUF INTEGER,
    regiao TEXT,
    codMesorregiao INTEGER,
    codMicrorregiao INTEGER,
    FOREIGN KEY (codUF) REFERENCES tb_UF (codUF),
    FOREIGN KEY (codMesorregiao) REFERENCES tb_Mesorregiao (codMesorregiao),
    FOREIGN KEY (codMicrorregiao) REFERENCES tb_Microrregiao (codMicrorregiao)
);

CREATE TABLE tb_instituicao (
    regiao TEXT,
    codRegiao INTEGER,
    UF TEXT,
    codUF INTEGER,
    municipio TEXT,
    codMunicipio INTEGER,
    entidade TEXT,
    codEntidade INTEGER,
    matriculas_base INTEGER,
    ano INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
     PRIMARY KEY (codEntidade, ano),
    FOREIGN KEY (codMunicipio) REFERENCES tb_Municipio (idMunicipio)
);
