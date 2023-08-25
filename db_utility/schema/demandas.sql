CREATE TABLE Demandas (
    demanda_id INTEGER PRIMARY KEY,
    ans INTEGER NOT NULL ,
    razao_social VARCHAR(140) NOT NULL,
    beneficiarios INTEGER,
    data_atendimento_demanda DATE,
    classificacao_demanda VARCHAR(25),
    natureza_demanda VARCHAR(25),
    subtema_demanda VARCHAR(250)
)