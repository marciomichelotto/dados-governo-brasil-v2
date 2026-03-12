# Arquitetura técnica (ingestão local + consumo analítico)

## Visão geral

A arquitetura atual é orientada a execução via CLI, com foco em ingestão de um arquivo CSV,
transformação leve em memória e carga em lotes para SQL Server, além de consumo analítico em Snowflake via SQL documentado.

```mermaid
flowchart LR
    A[Arquivo CSV\n(caminho local)] --> B[Leitura com pandas.read_csv]
    B --> C[Transformação\nclean_dataframe]
    C --> D[Inferência de tipos\ninfer_sqlalchemy_types]
    D --> E[Carga em lotes\nDataFrame.to_sql + SQLAlchemy/pyodbc]
    E --> F[Tabela SQL Server\n(schema.tabela)]
    E --> G[Logs de execução\n(logging)]
    F --> H[Camada de consumo\nqueries analíticas]
    H --> I[Snowflake\nscript SQL e KPIs]
```

## Componentes

- **Entrada (CSV):** arquivo delimitado (`--delimiter`) e codificado (`--encoding`) lido via `pandas`.
- **Transformação:** normalização de nomes de colunas, trim de strings, remoção de linhas vazias e deduplicação opcional.
- **Mapeamento de tipos:** inferência automática para tipos SQLAlchemy antes da persistência.
- **Persistência:** escrita no SQL Server em batches (`--chunksize`) com políticas de existência (`--if-exists`).
- **Observabilidade:** logs das etapas principais e tempo total da execução.
- **Consumo analítico:** consultas e modelagem SQL orientadas ao Snowflake no estudo de caso `DESPESAS_ORGAO`.

## Limites atuais da arquitetura

1. **Processamento majoritariamente em memória:** pode pressionar RAM em CSVs muito grandes.
2. **Sem orquestração nativa:** execução manual por CLI, sem agendamento embutido.
3. **Qualidade de dados por regras genéricas:** ainda sem contratos de schema por domínio.
4. **Recuperação de falhas básica:** não há mecanismo de retry transacional por lote.

## Roadmap técnico sugerido

### Curto prazo

- Adicionar validações opcionais por coluna (regras de domínio).
- Publicar métricas de execução por etapa (linhas lidas, removidas, carregadas).
- Criar modo "dry-run" para validar parsing e schema sem gravar no banco.

### Médio prazo

- Isolar camadas de **ingestão**, **transformação** e **persistência** em módulos independentes.
- Introduzir configuração central via arquivo (`yaml/toml`) além da CLI.
- Adicionar suporte a carga incremental por watermark (quando aplicável).

### Longo prazo

- Orquestrar com scheduler/workflow (ex.: Airflow, Prefect ou GitHub Actions agendado).
- Adicionar data quality framework (ex.: Great Expectations/Pandera).
- Evoluir para arquitetura híbrida com staging em object storage e processamento distribuído.
