# Relatório de Métricas Estatísticas e Econométricas — TCC Lido DAO & Liquid Staking
**Recorte Temporal:** Maio de 2022 a Abril de 2026 (48 Meses)  
**Data de Geração:** 2026-08-05 12:23:24  

---

## 1. Estatísticas Descritivas do Depeg stETH/ETH (Maio/2022 a Abril/2026)

| Métrica | Valor | Observação |
|---|---|---|
| **Total de Observações (Dias)** | 1313 | Recorte Maio/2022 – Abril/2026 |
| **Preço Médio (stETH/ETH)** | 0.995941 | Paridade nominal teórica: 1.000000 |
| **Depeg Médio (%)** | -0.4059% | Média de desvio no período |
| **Depeg Mediano (%)** | -0.1054% | - |
| **Desvio Padrão (%)** | 1.6837% | Volatilidade temporal do peg |
| **Maior Desconto / Depeg Mínimo (%)** | -13.0469% | Registrado durante o colapso Terra/LUNA |
| **Maior Prêmio / Depeg Máximo (%)** | 14.2740% | Registrado pós-insolvência da FTX |
| **Assimetria (Skewness)** | -0.3473 | Negativa (cauda longa em desvalorizações) |
| **Curtose (Kurtosis)** | 15.7141 | Leptocúrtica (caudas pesadas) |
| **Autocorrelação AR(1)** | 0.2363 | Inércia de depeg no curto prazo |
| **Autocorrelação AR(5)** | 0.2497 | Persistência de liquidez a médio prazo |

### Distribuição Percentílica do Depeg (%)
- **Percentil 1% (Worst 1%):** -5.6159%
- **Percentil 5%:** -3.3491%
- **Percentil 25% (Q1):** -0.3650%
- **Percentil 75% (Q3):** -0.0173%
- **Percentil 95%:** 0.9874%
- **Percentil 99%:** 5.0161%

---

## 2. Impacto do Upgrade Shanghai/Capella (Habilitação de Saques Nativos em 12/04/2023)

| Parâmetro | Pré-Shanghai (Sem Saques: Maio/22 - Abr/23) | Pós-Shanghai (Com Saques: Abr/23 - Abr/26) | Impacto / Teste |
|---|---|---|---|
| **Período** | 2022-05-01 a 2023-04-12 | 2023-04-13 a 2026-04-30 | - |
| **Dias Analisados** | 309 | 1004 | - |
| **Depeg Médio (%)** | -1.3860% | -0.1042% | t-stat: -9.88 (p: 1.0458e-20) |
| **Desvio Padrão (%)** | 2.1470% | 1.3804% | **Redução de 35.7% na volatilidade** |
| **Depeg Mínimo (%)** | -12.3277% | -13.0469% | Eliminação de desvios extremos |
| **Dias com Depeg < -2%** | 94 (30.4%) | 56 (5.6%) | Estabilização da arbitragem 1:1 |

---

## 3. Comportamento em Janelas de Estresse Sistêmico

| Evento de Mercado | Período | Depeg Médio (%) | Depeg Mínimo (%) | Desvio Padrão (%) |
|---|---|---|---|---|
| **Crash Terra/LUNA (Maio 2022)** | 2022-05-01 a 2022-05-31 | -1.8011% | **-12.3277%** | 2.2242% |
| **Insolvência Celsius / Depeg de Verão (Junho 2022)** | 2022-06-01 a 2022-06-30 | -3.7047% | **-11.1644%** | 2.5941% |
| **Colapso FTX (Novembro 2022)** | 2022-11-01 a 2022-11-30 | -0.9052% | **-4.5541%** | 1.6677% |
| **Upgrade Shanghai / Saques (Abril 2023)** | 2023-04-01 a 2023-04-30 | -0.2122% | **-0.6623%** | 0.2666% |
| **Hack KelpDAO / Crise Restaking (Abril 2026)** | 2026-04-15 a 2026-04-30 | -0.1285% | **-0.8667%** | 0.9444% |

---

## 4. Análise de Rendimentos (Lido APR vs. Solo Staking Direto)

| Métrica | Lido stETH | Solo Staking Direto (Estimado) | Spread / Custo Lido DAO |
|---|---|---|---|
| **Rendimento Médio (APR/APY %)** | 3.54% | 3.93% | **0.393%** |
| **Rendimento Mínimo (%)** | 2.28% | 2.54% | - |
| **Rendimento Máximo (%)** | 11.77% | 13.08% | - |
| **Desvio Padrão (%)** | 1.04% | - | Tracking Error: 0.1158% |

---

## 5. Concentração de Mercado, HHI e Risco de Governança

- **Market Share Médio da Lido DAO (Maio/22 - Abr/26):** **78.65%**
- **Índice Herfindahl-Hirschman (HHI) Médio:** **6478.2** (Mercado Altamente Concentrado > 2500)
### Correlação Estatística (Market Share Lido vs Depeg stETH)
- **Coeficiente de Pearson (r):** `-0.1951` (p-value: `1.0043e-12`)
- **Coeficiente de Spearman (r_s):** `-0.2411` (p-value: `8.1962e-19`)
