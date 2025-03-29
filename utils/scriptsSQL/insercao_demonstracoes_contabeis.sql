INSERT INTO
    demonstracoes_contabeis (
        DATA,
        REG_ANS,
        CD_CONTA_CONTABIL,
        DESCRICAO,
        VL_SALDO_INICIAL,
        VL_SALDO_FINAL
    )
VALUES
    (%s, %s, %s, %s, %s, %s);