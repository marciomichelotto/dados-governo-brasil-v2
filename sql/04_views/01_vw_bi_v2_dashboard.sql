CREATE OR REPLACE VIEW GOV_V2.GOVERNO.VW_BI_V2_DASHBOARD AS
SELECT
    MES_ANO,
    SUBSTR(MES_ANO, 5, 2)                                           AS ANO,
    SUBSTR(MES_ANO, 1, 3)                                           AS MES,
    CASE SUBSTR(MES_ANO, 1, 3)
        WHEN 'jan' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '01'
        WHEN 'fev' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '02'
        WHEN 'mar' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '03'
        WHEN 'abr' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '04'
        WHEN 'mai' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '05'
        WHEN 'jun' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '06'
        WHEN 'jul' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '07'
        WHEN 'ago' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '08'
        WHEN 'set' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '09'
        WHEN 'out' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '10'
        WHEN 'nov' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '11'
        WHEN 'dez' THEN '20' || SUBSTR(MES_ANO, 5, 2) || '12'
    END                                                             AS ANO_MES_SORT,
    ORGAO_SUPERIOR,
    ORGAO_ENTIDADE_VINCULADA,
    CASE
        WHEN ORGAO_SUPERIOR LIKE '%Saúde%'                                THEN 'SAÚDE'
        WHEN ORGAO_SUPERIOR LIKE '%Educação%'                             THEN 'EDUCAÇÃO'
        WHEN ORGAO_SUPERIOR LIKE '%Defesa%'                               THEN 'DEFESA'
        WHEN ORGAO_SUPERIOR LIKE '%Justiça%' OR ORGAO_SUPERIOR LIKE '%Segurança%' THEN 'SEGURANÇA'
        WHEN ORGAO_SUPERIOR LIKE '%Fazenda%'                              THEN 'FAZENDA'
        WHEN ORGAO_SUPERIOR LIKE '%Previdência%'                          THEN 'PREVIDÊNCIA'
        WHEN ORGAO_SUPERIOR LIKE '%Desenvolvimento Social%'               THEN 'DESENV. SOCIAL'
        ELSE 'OUTROS'
    END AS PILAR_ESTRATEGICO,
    VALOR_EMPENHADO,
    VALOR_LIQUIDADO,
    VALOR_PAGO,
    VALOR_RESTOS_PAGAR_PAGOS,
    ROUND(VALOR_PAGO / NULLIF(VALOR_EMPENHADO, 0) * 100, 2)         AS TAXA_EXECUCAO_PCT,
    ROUND(VALOR_RESTOS_PAGAR_PAGOS
        / NULLIF(VALOR_PAGO + VALOR_RESTOS_PAGAR_PAGOS, 0) * 100, 2) AS PCT_RESTOS_PAGAR,
    VALOR_PAGO - VALOR_EMPENHADO                                    AS GAP_EXECUCAO,
    CASE
        WHEN VALOR_RESTOS_PAGAR_PAGOS
            / NULLIF(VALOR_PAGO + VALOR_RESTOS_PAGAR_PAGOS, 0) > 0.50 THEN 'COLAPSO'
        WHEN VALOR_RESTOS_PAGAR_PAGOS
            / NULLIF(VALOR_PAGO + VALOR_RESTOS_PAGAR_PAGOS, 0) > 0.25 THEN 'RISCO'
        WHEN VALOR_RESTOS_PAGAR_PAGOS
            / NULLIF(VALOR_PAGO + VALOR_RESTOS_PAGAR_PAGOS, 0) > 0.10 THEN 'ATENÇÃO'
        WHEN VALOR_RESTOS_PAGAR_PAGOS
            / NULLIF(VALOR_PAGO + VALOR_RESTOS_PAGAR_PAGOS, 0) > 0.05 THEN 'MODERADO'
        ELSE 'EXEMPLAR'
    END AS STATUS_RISCO
FROM GOV_V2.GOVERNO.DESPESAS_GOV
WHERE ORGAO_SUPERIOR IS NOT NULL;
