CREATE TABLE IndiceGeralReclamacoes (
    ans INTEGER NOT NULL ,
    cobertura_operadora VARCHAR(50),
    porte_operadora VARCHAR(7),
    mes INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    indicador DOUBLE,
    PRIMARY KEY (ans, mes, ano),
    FOREIGN KEY (ans) REFERENCES Operadoras(ans)
)