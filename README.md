# Dados Governo Brasil v2

Projeto de engenharia e análise de dados com foco em **aprendizado prático de Snowflake**,
mantendo uma trilha complementar de ingestão em SQL Server para comparação de arquitetura e execução local.

## Requisitos

- Python 3.10+
- Driver ODBC do SQL Server instalado (ex.: ODBC Driver 18 for SQL Server)

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Estratégia do projeto (duas trilhas)

Este repositório foi organizado para deixar explícitas duas trilhas:

1. **Trilha de ingestão e qualidade em Python + SQL Server**
   - objetivo: praticar leitura de CSV, limpeza, tipagem e carga em lotes.
2. **Trilha analítica em Snowflake**
   - objetivo: praticar modelagem SQL analítica, validações de carga e consultas de negócio em ambiente cloud.

Assim, o projeto não trata Snowflake como apêndice: ele é a trilha principal de evolução analítica, enquanto o pipeline em SQL Server serve como base de engenharia e contraste técnico.

## Pipeline CSV -> SQL Server

Script principal: `pipeline/csv_to_sqlserver_pipeline.py`

### O que o pipeline faz

1. Lê um CSV com `pandas`.
2. Limpa os dados:
   - normaliza nomes de colunas para `snake_case`;
   - remove espaços extras em colunas de texto;
   - remove linhas totalmente vazias;
   - remove duplicatas (opcional).
3. Carrega no SQL Server com `SQLAlchemy` + `pyodbc` em lotes (`chunksize`).
4. Registra logs de execução (leitura, limpeza e carga) com tempo total.

### Exemplo de execução

```bash
python pipeline/csv_to_sqlserver_pipeline.py \
  --csv-path dados/entrada.csv \
  --connection-string "mssql+pyodbc://usuario:senha@servidor:1433/banco?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes" \
  --table tabela_destino \
  --schema dbo \
  --if-exists append \
  --chunksize 2000
```

### String de conexão via variável de ambiente

Para evitar exposição de credenciais no histórico do shell, você pode definir:

```bash
export DATABASE_URL="mssql+pyodbc://usuario:senha@servidor:1433/banco?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
```

E então executar sem `--connection-string`:

```bash
python pipeline/csv_to_sqlserver_pipeline.py \
  --csv-path dados/entrada.csv \
  --table tabela_destino
```

### Parâmetros principais

- `--csv-path`: caminho do arquivo CSV.
- `--connection-string`: string SQLAlchemy de conexão com SQL Server (opcional se `DATABASE_URL` estiver definida).
- `--table`: tabela de destino.
- `--schema`: schema de destino (default: `dbo`).
- `--if-exists`: comportamento se tabela existir (`fail`, `replace`, `append`).
- `--delimiter`: delimitador do CSV (default: `,`).
- `--encoding`: encoding do CSV (default: `utf-8`).
- `--chunksize`: linhas por lote (default: `1000`).
- `--keep-duplicates`: mantém duplicatas (por padrão, remove).

## Testes automatizados

O projeto possui testes com `pytest` para:

- limpeza de DataFrame;
- inferência de tipos SQLAlchemy;
- leitura de CSV com delimitador/encoding customizados;
- validação de argumentos do pipeline.

Rodar localmente:

```bash
pytest -q
```

## CI

Há workflow de CI em `.github/workflows/ci.yml` executando testes em push e pull request.

## Arquitetura

A documentação de arquitetura técnica do fluxo (entrada, transformação, carga e consumo) está em:

- `docs/arquitetura.md`

O documento também descreve os limites atuais e um roadmap técnico por horizonte (curto, médio e longo prazo).

## SQL para Snowflake (DESPESAS_ORGAO)

Incluímos um script SQL consolidado para criação da tabela, carga, validações e análises:

- `docs/snowflake_despesas_orgao.sql`

Também adicionamos sugestões de leitura de negócio e evolução técnica:

- `docs/insights_despesas_orgao.md`

## Se sua conta trial do Snowflake expirou

Você **não precisa bloquear o projeto** por causa disso. Há três caminhos práticos:

1. **Continuar evoluindo localmente (sem Snowflake ativo):**
   - mantenha o pipeline Python + SQL Server para praticar ingestão, validação e qualidade.
2. **Usar Snowflake apenas para estudo de SQL/modelagem (sem executar):**
   - evolua o script em `docs/snowflake_despesas_orgao.sql` e documente decisões de design.
3. **Criar nova conta para validação end-to-end em cloud:**
   - recomendado quando você quiser comprovar execução real de carga e performance no ambiente Snowflake.

Em resumo: **nova conta é recomendada para validar execução real no Snowflake, mas não é obrigatória para continuar aprendendo e evoluindo a documentação técnica agora**.

## Observações

- Para grandes volumes, ajuste `--chunksize` conforme CPU/memória/rede.
- Valide tipos inferidos no destino caso existam colunas sensíveis (datas, valores monetários, IDs).
