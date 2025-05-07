DROP TABLE IF EXISTS tb_instituicao;

CREATE TABLE tb_instituicao (
   regiao TEXT,
    codRegiao INTEGER,
    UF TEXT,
    codUF INTEGER,
    municipio TEXT,
    codMunicipio INTEGER,
    mesoregiao TEXT,
    codMesoregiao INTEGER,
    microregiao TEXT,
    codMicroregiao INTEGER,
    entidade TEXT,
    codEntidade INTEGER PRIMARY KEY AUTOINCREMENT,
    matriculas_base INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);