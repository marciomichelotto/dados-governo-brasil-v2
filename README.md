# 📊 Dados Governo Brasil v2

Pipeline de dados públicos do governo federal brasileiro — da ingestão em CSV até insights analíticos sobre **R$ 4,83 trilhões em despesas** de 36 ministérios.

---

## 🎯 Objetivo

Transformar dados orçamentários brutos do governo federal em informação estruturada e analisável — evidenciando padrões de execução, concentração de recursos e riscos fiscais por ministério.

Este projeto cobre o ciclo completo:

```
CSV (Portal da Transparência) → Python (limpeza + ingestão) → SQL Server → Análise SQL → Insights
```

---

## 🔍 Principais Descobertas (Exercício 2025)

### 1. Concentração Extrema de Recursos

Os 3 maiores ministérios concentram **90,8% de todo o orçamento federal**.

| Posição | Ministério | Pago (2025) | % do Total |
|--------|-----------|------------|-----------|
| 🥇 | Fazenda | R$ 2,67 trilhões | 61,2% |
| 🥈 | Previdência Social | R$ 1,07 trilhão | 24,5% |
| 🥉 | Saúde | R$ 224,4 bilhões | 5,1% |
| 4º | Educação | R$ 204,9 bilhões | 4,7% |
| 5º | Desenvolvimento Social | R$ 167,6 bilhões | 3,8% |

> 💡 **Insight:** O Ministério da Fazenda não é um ministério operacional — sua função principal é gerenciar a dívida pública federal. Aproximadamente 60-67% dos seus R$ 2,67 trilhões referem-se a amortização de dívida, não a políticas públicas.

---

### 2. Crise de Execução: Ministérios em Colapso Orçamentário

"Restos a pagar" representam dívidas de anos anteriores pagas no exercício atual. Percentuais altos indicam falha de planejamento ou incapacidade de execução.

**Situação Crítica (>50% de dívidas passadas):**

| Ministério | % Restos a Pagar | Status |
|-----------|-----------------|--------|
| Ministério das Mulheres | 64,18% | 🔴 CRÍTICO |
| Ministério do Esporte | 62,94% | 🔴 CRÍTICO |
| Ministério do Turismo | 60,69% | 🔴 CRÍTICO |
| Ministério do Empreendedorismo | 53,93% | 🔴 CRÍTICO |

> 💡 **Insight:** Esses ministérios operam majoritariamente para quitar dívidas antigas — com capacidade limitada para novos programas. É um ciclo vicioso: sem execução no ano, acumulam dívida; no ano seguinte, gastam o orçamento pagando o passado.

---

### 3. Alerta Crítico: Receita Federal com 24,43% de Execução

| Métrica | Valor |
|--------|-------|
| Empenhado | R$ 11,7 bilhões |
| Efetivamente Pago | R$ 2,86 bilhões |
| Recursos Não Executados | **R$ 8,8 bilhões parados** |
| Restos a Pagar | 16,33% |

> 💡 **Insight:** A baixa execução da Receita Federal compromete diretamente sua capacidade de fiscalização e arrecadação — um problema fiscal que se retroalimenta. R$ 8,8 bilhões não executados em sistemas, fiscalização e infraestrutura representam perda de arrecadação potencial não mensurável.

---

### 4. Paradoxo do Tamanho: Grandes Ministérios Executam Melhor

Contraintuitivamente, os maiores ministérios apresentam a **melhor** gestão orçamentária proporcional:

| Ministério | Taxa de Execução | % Restos a Pagar | Avaliação |
|-----------|-----------------|-----------------|----------|
| Fazenda | 97,32% | 1,52% | ✅ Excelente |
| Previdência Social | 94,36% | 5,89% | ✅ Bom |
| Saúde | 90,23% | 10,07% | ⚠️ Aceitável |
| Educação | 84,58% | 14,49% | ⚠️ Atenção |

**Benchmarks de gestão exemplar (<5% de restos):**

| Ministério | % Restos a Pagar |
|-----------|-----------------|
| Desenvolvimento Social | 0,77% 🏆 |
| Fazenda | 1,49% |
| Trabalho e Emprego | 2,76% |
| Relações Exteriores | 3,23% |

> 💡 **Insight:** O padrão de excelência existe — Desenvolvimento Social com 0,77% de restos a pagar prova que é possível. O desafio é escalar essa capacidade para ministérios menores, especialmente os de criação recente.

---

## 🛠️ Stack Técnica

| Ferramenta | Uso |
|-----------|-----|
| Python (pandas + SQLAlchemy) | Limpeza, transformação e ingestão de CSVs |
| SQL Server | Data warehouse local — armazenamento permanente |
| Snowflake | Queries analíticas exploratórias e views consolidadas |
| SQL | Análise, agregações e geração de indicadores |
| Git | Versionamento |

---

## ⚙️ Pipeline

### Estrutura

```
dados-governo-brasil-v2/
│
├── pipeline/
│   └── csv_to_sqlserver_pipeline.py   # Ingestão CSV → SQL Server
│
├── docs/
│   ├── snowflake_despesas_orgao.sql   # Queries analíticas
│   └── insights_despesas_orgao.md     # Análise de negócio
│
├── requirements.txt
└── README.md
```

### O que o pipeline faz

1. Lê CSV do Portal da Transparência com `pandas`
2. Normaliza colunas para `snake_case`
3. Remove espaços, linhas vazias e duplicatas
4. Carrega no SQL Server via `SQLAlchemy` + `pyodbc` em lotes configuráveis

### Execução

```bash
pip install -r requirements.txt

python pipeline/csv_to_sqlserver_pipeline.py \
  --csv-path dados/despesasPorOrgao.csv \
  --connection-string "mssql+pyodbc://usuario:senha@servidor/banco?driver=ODBC+Driver+18+for+SQL+Server" \
  --table despesas_orgao \
  --schema dbo \
  --if-exists replace \
  --chunksize 2000
```

---

## 📌 Fonte dos Dados

- **Portal da Transparência do Governo Federal:** [transparencia.gov.br](https://www.transparencia.gov.br)
- **Exercício:** 2025
- **Escopo:** 36 ministérios — R$ 4,83 trilhões em despesas

---

## 👤 Autor

**Márcio Michelotto**
Engenheiro & Analista de Dados | [LinkedIn](https://www.linkedin.com/in/marciomichelotto-dados) | [GitHub](https://github.com/marciomichelotto)

---

*Projeto de análise de dados públicos — ciclo completo de engenharia e análise orçamentária.*
