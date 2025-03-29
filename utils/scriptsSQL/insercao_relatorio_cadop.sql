INSERT INTO
    relatorio_cadop (
        REG_ANS,
        CNPJ,
        RAZAO_SOCIAL,
        NOME_FANTASIA,
        MODALIDADE,
        LOGRADOURO,
        NUMERO,
        COMPLEMENTO,
        BAIRRO,
        CIDADE,
        UF,
        CEP,
        DDD,
        TELEFONE,
        FAX,
        ENDERECO_ELETRONICO,
        REPRESENTANTE,
        CARGO_REPRESENTANTE,
        REGIAO_COMERCIALIZACAO,
        DATA_REG_ANS
    )
VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)