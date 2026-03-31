# Dados Governo Brasil V2

Projeto de análise de despesas do Governo Federal do Brasil utilizando Snowflake.

## Objetivo

Ingestão, transformação e análise das despesas públicas por órgão do governo federal, com classificação por pilar estratégico e indicadores de risco fiscal.

## Arquitetura

Portal da Transparência (CSV) -> Snowflake Stage (`@GOV_STAGE`) -> Tabela `DESPESAS_GOV` (raw) -> View `VW_BI_V2_DASHBOARD` (analytics) -> Dashboard BI

## Estrutura do Repositório

```text
dados-governo-brasil-v2/
├── README.md
├── sql/
│   ├── 01_setup/
│   │   ├── 01_create_database.sql
│   │   ├── 02_create_schema.sql
│   │   ├── 03_create_file_format.sql
│   │   └── 04_create_stage.sql
│   ├── 02_tables/
│   │   ├── 01_despesas_gov.sql
│   │   └── 02_despesas_orgao.sql
│   ├── 03_load/
│   │   └── 01_copy_into_despesas.sql
│   └── 04_views/
│       └── 01_vw_bi_v2_dashboard.sql
└── data/
    └── despesasPorOrgao.csv
```

## Objetos Snowflake

| Tipo | Nome | Descrição |
|------|------|-----------|
| Database | `GOV_V2` | Banco de dados principal |
| Schema | `GOVERNO` | Schema de despesas governamentais |
| Table | `DESPESAS_GOV` | Despesas por órgão (3.044 registros) |
| Table | `DESPESAS_ORGAO` | Tabela auxiliar de despesas por órgão |
| View | `VW_BI_V2_DASHBOARD` | View analítica com KPIs e classificação de risco |
| Stage | `GOV_STAGE` | Stage interno para ingestão de CSVs |
| File Format | `GOV_CSV_FORMAT` | Formato CSV com `SKIP_HEADER = 1` |

## Colunas da Tabela DESPESAS_GOV

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `MES_ANO` | VARCHAR(7) | Período no formato `mmm/aa` (ex: `mar/25`) |
| `ORGAO_SUPERIOR` | VARCHAR(200) | Código e nome do órgão superior |
| `ORGAO_ENTIDADE_VINCULADA` | VARCHAR(200) | Entidade vinculada ao órgão |
| `VALOR_EMPENHADO` | NUMBER(38,2) | Valor empenhado (R$) |
| `VALOR_LIQUIDADO` | NUMBER(38,2) | Valor liquidado (R$) |
| `VALOR_PAGO` | NUMBER(38,2) | Valor efetivamente pago (R$) |
| `VALOR_RESTOS_PAGAR_PAGOS` | NUMBER(38,2) | Restos a pagar processados (R$) |

## KPIs da View VW_BI_V2_DASHBOARD

| Indicador | Fórmula | Descrição |
|-----------|---------|-----------|
| `TAXA_EXECUCAO_PCT` | `VALOR_PAGO / VALOR_EMPENHADO * 100` | Taxa de execução orçamentária |
| `PCT_RESTOS_PAGAR` | `RESTOS / (PAGO + RESTOS) * 100` | Proporção de restos a pagar |
| `GAP_EXECUCAO` | `VALOR_PAGO - VALOR_EMPENHADO` | Diferença entre pago e empenhado |
| `STATUS_RISCO` | Baseado em `PCT_RESTOS_PAGAR` | Classificação de risco fiscal |

## Classificação de Risco (STATUS_RISCO)

| Status | Condição (% Restos a Pagar) |
|--------|----------------------------|
| COLAPSO | > 50% |
| RISCO | > 25% |
| ATENÇÃO | > 10% |
| MODERADO | > 5% |
| EXEMPLAR | ≤ 5% |

## Pilares Estratégicos

Os órgãos são classificados automaticamente em pilares:

- **SAÚDE** — Ministério da Saúde
- **EDUCAÇÃO** — Ministério da Educação
- **DEFESA** — Ministério da Defesa
- **SEGURANÇA** — Justiça e Segurança Pública
- **FAZENDA** — Ministério da Fazenda
- **PREVIDÊNCIA** — Previdência Social
- **DESENV. SOCIAL** — Desenvolvimento Social
- **OUTROS** — Demais órgãos

## Como Executar

1. Execute os scripts na ordem numérica:

```text
sql/01_setup/ → sql/02_tables/ → sql/03_load/ → sql/04_views/
```

2. Faça upload do CSV para o stage:

```sql
PUT file://despesasPorOrgao.csv @GOV_V2.GOVERNO.GOV_STAGE;
```

3. Execute o `COPY INTO` para carregar os dados.
4. A view estará disponível para consultas e dashboards.

## Fonte dos Dados

Portal da Transparência — Despesas do Governo Federal.

## Tecnologias

- Snowflake — Data Warehouse
- SQL — Transformação e análise
