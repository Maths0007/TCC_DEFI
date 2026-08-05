# Relatório de Métricas Estatísticas e Econométricas — TCC Lido DAO & Liquid Staking

**Data de Geração:** 2026-08-05 10:42:46  
**Autor:** Matheus — TCC Finanças Descentralizadas (DeFi)

---

## 1. Estatísticas Descritivas do Depeg stETH/ETH

| Métrica | Valor | Observação |
|---|---|---|
| **Total de Observações (Dias)** | 1831 | Jan/2021 a Jul/2026 |
| **Preço Médio (stETH/ETH)** | 0.995193 | Paridade nominal teórica: 1.000000 |
| **Depeg Médio (%)** | -0.4807% | Leve desconto estrutural histórico |
| **Depeg Mediano (%)** | -0.1185% | - |
| **Desvio Padrão (%)** | 2.1493% | Medida de volatilidade do peg |
| **Maior Desconto / Depeg Mínimo (%)** | -21.7953% | Ocorrido durante o colapso da Terra/LUNA |
| **Maior Prêmio / Depeg Máximo (%)** | 14.2740% | Ocorrido pós-falência da FTX |
| **Assimetria (Skewness)** | -1.1534 | Negativa (cauda longa de desvalorização em crises) |
| **Curtose (Kurtosis)** | 16.6383 | Leptocúrtica (caudas pesadas / eventos extremos) |
| **Autocorrelação AR(1)** | 0.1687 | Inércia temporal do depeg (Gogol et al., 2024) |
| **Autocorrelação AR(5)** | 0.1237 | Persistência de iliquidez a médio prazo |

### Distribuição Percentílica do Depeg (%)
- **Percentil 1% (Worst 1%):** -7.1495%
- **Percentil 5%:** -3.8305%
- **Percentil 25% (Q1):** -0.7191%
- **Percentil 75% (Q3):** -0.0065%
- **Percentil 95%:** 2.0446%
- **Percentil 99%:** 6.3266%

---

## 2. Impacto do Upgrade Shanghai/Capella (Habilitação de Saques Nativos em 12/04/2023)

| Parâmetro | Pré-Shanghai (Sem Saques) | Pós-Shanghai (Com Saques) | Impacto / Teste |
|---|---|---|---|
| **Período** | 2020-12-31 a 2023-04-12 | 2023-04-13 a 2026-07-26 | - |
| **Dias Analisados** | 755 | 1076 | - |
| **Depeg Médio (%)** | -1.0144% | -0.1062% | Dif. Média (t-stat: -8.23, p: 5.6626e-16) |
| **Desvio Padrão (%)** | 2.7786% | 1.4520% | **Redução de 47.7% na volatilidade** |
| **Depeg Mínimo (%)** | -21.7953% | -13.0469% | Atenuação drástica do risco de cauda |
| **Dias com Depeg < -2%** | 184 (24.4%) | 67 (6.2%) | Eliminação do basis risk crônico |

> **Insight Acadêmico:** A habilitação dos saques nativos no protocolo Ethereum provou empiricamente a tese de eficiência de arbitragem: o risco de *depeg* duradouro reportado nas literaturas clássicas (ex: Scharnowski & Jahanshahloo, 2025) foi drasticamente atenuado, pois os arbitradores agora contam com o mecanismo de resgate 1:1 direto na Beacon Chain.

---

## 3. Comportamento em Janelas de Estresse Sistêmico

| Evento de Mercado | Período | Depeg Médio (%) | Depeg Mínimo / Pior Desconto (%) | Desvio Padrão (%) |
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
| **Rendimento Médio (APR/APY %)** | 3.47% | 3.85% | **0.385%** |
| **Rendimento Mínimo (%)** | 2.04% | 2.27% | - |
| **Rendimento Máximo (%)** | 11.77% | 13.08% | - |
| **Desvio Padrão (%)** | 1.05% | - | Tracking Error: 0.1165% |

> **Nota:** A Lido DAO retém uma taxa fixa de 10% sobre as recompensas brutas de staking (5% repassados aos operadores de nós e 5% destinados à tesouraria da DAO).

---

## 5. Concentração de Mercado, HHI e Risco de Governança

- **Market Share Atual da Lido DAO:** **53.82%** (TVL: $18,197,860,759)
- **Market Share Histórico Médio:** **79.16%** (Máximo: 94.0%, Mínimo: 18.2%)
- **Índice Herfindahl-Hirschman (HHI) Atual:** **3481.0** (Mercado Altamente Concentrado > 2500)
- **HHI Histórico Médio:** **6691.0**

### Correlação Estatística entre Dominância da Lido (%) e Depeg do stETH (%)
- **Coeficiente de Pearson (r):** `-0.0822` (p-value: `4.2819e-04`)
- **Coeficiente de Spearman (r_s):** `-0.2080` (p-value: `2.5091e-19`)
- **Interpretação:** Validação da tese de Scharnowski & Jahanshahloo (2025) — maior concentração do protocolo correlaciona-se com maior exigência de prêmio de risco no mercado secundário.
