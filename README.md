# 🏛️ Análise de Dados Orçamentários do Governo Federal - V2

[![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=flat&logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-Advanced-orange?style=flat)](https://en.wikipedia.org/wiki/SQL)

## 🚀 Sobre o Projeto

Análise avançada dos gastos públicos federais brasileiros utilizando **Snowflake Data Cloud**, com foco em execução orçamentária de Ministérios e órgãos federais.

### 📊 Evolução do Projeto

Este projeto é uma **evolução significativa** da [versão inicial](link-do-repo-antigo) criada em 2021. 

#### Comparação V1 vs V2:

| Aspecto | V1 (2021) | V2 (2024-2025) |
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

## 📂 Estrutura do Projeto
```
├── snowflake/          # Scripts SQL do Snowflake
├── scripts/            # Scripts Python de análise
├── notebooks/          # Jupyter notebooks exploratórios
├── relatorios/         # Relatórios em Markdown
├── visualizacoes/      # Gráficos e dashboards
└── docs/               # Documentação técnica
```

## 🚀 Como Usar

### Pré-requisitos
```bash
pip install -r requirements.txt
```

### Executar Análises
```bash
# Backup dos dados do Snowflake
python scripts/backup_snowflake.py

# Análise de órgãos não-ministeriais
python scripts/analise_orgaos.py

# Análise de ministérios
python scripts/analise_ministerios.py
```

## 📈 Principais Descobertas

- 🔴 **Presidência:** 82,7% do orçamento concentrado em dezembro
- 🟢 **Banco Central:** 98,83% de taxa de liquidação (benchmark)
- 📊 **Total analisado:** R$ 33,77 bilhões (órgãos não-ministeriais)

## 👨‍💻 Autor

**Márcio** - Analista de Dados  
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

- **V1 (2021):** [dados-governo-brasil-v1](link-repo-antigo) - Análise básica com CSV e Power BI
- **V2 (2024-2025):** Este repositório - Análise avançada com Snowflake
