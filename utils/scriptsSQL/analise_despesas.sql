WITH top_10_operadoras_despesas AS (
SELECT 
    reg_ans, SUM(vl_saldo_final - vl_saldo_inicial) AS despesas
FROM
    demonstracoes_contabeis
WHERE
    data BETWEEN (SELECT MAX(data) - INTERVAL %s MONTH FROM demonstracoes_contabeis) 
		AND 
        (SELECT MAX(data) FROM demonstracoes_contabeis)
	AND 
    descricao like 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
GROUP BY reg_ans
ORDER BY despesas DESC
LIMIT 10
)
SELECT r.razao_social AS "Operadora - Razão social", t.despesas as "Despesa anual"
FROM top_10_operadoras_despesas AS t 
LEFT JOIN relatorio_cadop AS r ON t.reg_ans = r.reg_ans