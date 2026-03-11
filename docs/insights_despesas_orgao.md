# Insights sugeridos para `DESPESAS_ORGAO`

Este documento resume hipóteses analíticas úteis a partir das queries consolidadas em `docs/snowflake_despesas_orgao.sql`.

## 1) Eficiência de execução orçamentária

**Métrica-chave:** `TAXA_EXECUCAO = VALOR_PAGO / VALOR_EMPENHADO`.

- Valores muito acima de 100% podem indicar:
  - pagamento de restos de exercícios anteriores;
  - reclassificações contábeis;
  - ou necessidade de investigação de qualidade dos dados.

## 2) Pressão de passivos (restos a pagar)

**Métrica-chave:** `PERCENTUAL_DIVIDA_PASSADA`.

- Quanto maior o percentual de `VALOR_RESTOS_PAGAR_PAGOS`, maior a parcela do desembolso comprometida com obrigações antigas.
- Isso ajuda a diferenciar ministérios com foco em execução do ano corrente versus “limpeza” de passivos.

## 3) Concentração de gasto por unidade vinculada

- Use o **Top 10 de unidades** para identificar concentração excessiva em poucos executores.
- Se a concentração for alta, vale explorar risco operacional e dependência institucional.

## 4) Sazonalidade mensal por pilar estratégico

- A série temporal por `ANO` e `MES` permite detectar:
  - picos sazonais de liquidação e pagamento;
  - aceleração de fim de ano;
  - divergência entre áreas (saúde, educação, defesa, segurança).

## 5) Sugestões de evolução técnica

- Criar **FILE FORMAT nomeado** no Snowflake para padronizar encoding/delimitador.
- Adotar **`TRY_TO_NUMBER`** durante carga inicial exploratória e registrar rejeições em tabela de erros.
- Materializar a view analítica em tabela incremental se o volume crescer.
- Padronizar `MES_ANO` em data (`DATE`) para facilitar BI e ordenações.
