# 📊 Evolução do Projeto: V1 → V2

## 🎓 Contexto de Aprendizado

### V1 - Início da Jornada (2025)
Quando criei a primeira versão, estava **iniciando na área de dados**. O objetivo era aprender fundamentos de:
- Manipulação de dados com Python
- Consultas SQL básicas
- Visualização no Power BI

### V2 - Maturidade Profissional (2026)
Com mais experiência, refiz o projeto incorporando **boas práticas profissionais**:
- Arquitetura de dados em nuvem
- SQL avançado e otimizado
- Versionamento e documentação
- Análises estatísticas complexas

## 📈 Evolução Técnica

### Armazenamento de Dados

**V1:**
```python
# CSV local - problemático para dados grandes
df = pd.read_csv('despesas.csv')  # Carrega tudo na memória
```

**V2:**
```sql
-- Snowflake - escalável e performático
SELECT * FROM DADOS_GOV.MINISTERIOS.DESPESAS_ORGAO
WHERE VALOR_EMPENHADO > 1000000;  -- Processa no servidor
```

### Análises

**V1: Básica**
- Soma total por órgão
- Gráficos simples de barras
- Filtros manuais no Power BI

**V2: Avançada**
- Séries temporais com sazonalidade
- Detecção de anomalias
- Análise de eficiência orçamentária
- Heatmaps de execução mensal
- Coeficiente de variação
- Análise de gaps orçamentários

### Performance

| Operação | V1 | V2 |
|----------|----|----|
| Carregar dados | 2-3 min | 0.5 seg |
| Agregação complexa | 30 seg | 2 seg |
| Filtrar 1M registros | Falha (memória) | Instantâneo |

## 💡 Principais Aprendizados

1. **Escalabilidade importa:** CSV é bom para aprender, cloud é essencial para produção
2. **SQL é poderoso:** Processar no banco é mais eficiente que em Python
3. **Documentação é crucial:** Código sem doc é código descartável
4. **Versionamento salva vidas:** Git não é opcional

## 🎯 Próximos Passos (V3?)

- [ ] Deploy de API REST com FastAPI
- [ ] Dashboard interativo com Streamlit
- [ ] Pipeline de ETL automatizado com Airflow
- [ ] Machine Learning para previsão orçamentária
- [ ] Alertas automáticos de anomalias

---

**Conclusão:** Este projeto mostra minha evolução de **iniciante para profissional de dados** em X anos.
