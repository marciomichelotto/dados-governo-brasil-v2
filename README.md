(EM CONSTRUÇÃO)

# 🏛️ Análise de Dados Orçamentários do Governo Federal - V2

[![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=flat&logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-Advanced-orange?style=flat)](https://en.wikipedia.org/wiki/SQL)

## 🚀 Sobre o Projeto

Análise avançada dos gastos públicos federais brasileiros utilizando **Snowflake Data Cloud**, com foco em execução orçamentária de Ministérios e órgãos federais.

### 📊 Evolução do Projeto

Este projeto é uma **evolução significativa** da [versão inicial](https://github.com/marciomichelotto/analise-gastos-governo) criada quando estava iniciando em análise de dados. 

#### Comparação V1 vs V2:

| Aspecto | V1 (2025) | V2 (2026) |
|---------|-----------|----------------|
| **Armazenamento** | CSV local (500 MB) | Snowflake Cloud (escalável) |
| **Processamento** | Pandas (memória limitada) | Snowflake SQL (massivo) |
| **Volume de dados** | ~100k registros | ~3M+ registros |
| **Visualização** | Power BI Desktop | Python + Matplotlib + Seaborn |
| **Versionamento** | Sem controle | Git + GitHub |
| **Automação** | Manual | Scripts Python automatizados |
| **Análise temporal** | Mensal básica | Séries temporais avançadas |
| **Performance** | ~5 min de processamento | ~2 segundos (queries) |

📖 **Leia mais:** [Documento completo de evolução](docs/comparacao_versoes.md)

## 🎯 Principais Análises

1. **Órgãos Não-Ministérios** (Presidência, AGU, BCB, CGU)
2. **Ministérios Federais** (26 ministérios)
3. **Análise Temporal** (tendências 2025)
4. **Eficiência Orçamentária** (liquidação e pagamento)

## 🛠️ Stack Tecnológica

- **Data Warehouse:** Snowflake
- **Linguagem:** Python 3.11+
- **Bibliotecas:** Pandas, Matplotlib, Seaborn
- **SQL:** Queries complexas para agregação
- **Versionamento:** Git/GitHub

## 📂 Estrutura dos Dados

### Database no Snowflake:
```
DADOS_GOV.MINISTERIOS.DESPESAS_ORGAO
```

### Colunas principais:
- `MES_ANO` - Mês/ano da despesa
- `ORGAO_SUPERIOR` - Órgão responsável
- `ORGAO_ENTIDADE_VINCULADA` - Entidade vinculada
- `VALOR_EMPENHADO` - Valor comprometido
- `VALOR_LIQUIDADO` - Valor reconhecido como obrigação
- `VALOR_PAGO` - Valor efetivamente pago
- `VALOR_RESTOS_PAGAR_PAGOS` - Pagamento de restos de exercícios anteriores

## 🔍 Queries SQL Utilizadas

### Listar órgãos não-ministeriais:
```sql
SELECT DISTINCT ORGAO_SUPERIOR
FROM DADOS_GOV.MINISTERIOS.DESPESAS_ORGAO
WHERE ORGAO_SUPERIOR NOT LIKE '%Ministério%'
ORDER BY ORGAO_SUPERIOR;
```

### Análise consolidada por órgão:
```sql
SELECT 
    ORGAO_SUPERIOR,
    COUNT(*) AS TOTAL_REGISTROS,
    SUM(VALOR_EMPENHADO) AS TOTAL_EMPENHADO,
    SUM(VALOR_LIQUIDADO) AS TOTAL_LIQUIDADO,
    SUM(VALOR_PAGO) AS TOTAL_PAGO,
    SUM(VALOR_RESTOS_PAGAR_PAGOS) AS TOTAL_RESTOS_PAGAR
FROM DADOS_GOV.MINISTERIOS.DESPESAS_ORGAO
WHERE ORGAO_SUPERIOR NOT LIKE '%Ministério%'
GROUP BY ORGAO_SUPERIOR
ORDER BY TOTAL_EMPENHADO DESC;
```

### Evolução temporal mensal:
```sql
SELECT 
    ORGAO_SUPERIOR,
    MES_ANO,
    SUM(VALOR_EMPENHADO) AS EMPENHADO_MES,
    SUM(VALOR_LIQUIDADO) AS LIQUIDADO_MES,
    SUM(VALOR_PAGO) AS PAGO_MES
FROM DADOS_GOV.MINISTERIOS.DESPESAS_ORGAO
WHERE ORGAO_SUPERIOR NOT LIKE '%Ministério%'
GROUP BY ORGAO_SUPERIOR, MES_ANO
ORDER BY ORGAO_SUPERIOR, MES_ANO;
```

## 📈 Principais Descobertas

- 🔴 **Presidência:** 82,7% do orçamento concentrado em dezembro
- 🟢 **Banco Central:** 98,83% de taxa de liquidação (benchmark)
- 📊 **Total analisado:** R$ 33,77 bilhões (órgãos não-ministeriais)

## 👨‍💻 Autor

**Márcio** - Engenheiro de Dados  
📧 Email: marciomichelotto@gmail.com  
💼 LinkedIn: www.linkedin.com/in/marciomichelotto-dados

## 📜 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Dados públicos do Portal da Transparência
- Snowflake Education Program
- Comunidade Python Brasil

---

### 🔄 Versões do Projeto

- **V1 (2025):** [versão inicial](https://github.com/marciomichelotto/analise-gastos-governo) - Análise básica com CSV e Power BI
- **V2 (2026):** Este repositório - Análise avançada com Snowflake
