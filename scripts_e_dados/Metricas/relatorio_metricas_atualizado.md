# Relatório de Métricas Estatísticas do TCC (Atualizado)

**Recorte Temporal Analisado:** 2022-05-01 a 2026-05-31 (1492 Dias Consecutivos)  
**Fonte dos Dados:** Beaconcha.in (Staked ETH e ETH.STORE APR) e Yahoo Finance (`ETH-USD`, `STETH-USD`).

---

## 1. Estatísticas Descritivas do Depeg stETH/ETH

| Indicador | Valor | Interpretação Acadêmica |
| :--- | :--- | :--- |
| **Total de Dias** | 1492 | Amostra diária completa sem lacunas |
| **Depeg Médio** | -0.5127% | Desconto médio estrutural pré/pós Shanghai |
| **Depeg Mediano** | -0.1267% | Paridade típica do mercado |
| **Desvio Padrão** | 0.9739% | Volatilidade temporal da paridade |
| **Maior Desconto (Mínimo)** | -6.3263% | Pico de estresse de liquidez (Crash Terra/LUNA e Celsius) |
| **Maior Prêmio (Máximo)** | 1.0851% | Máximo prêmio registrado |

### Distribuição Percentílica do Depeg:
- **P1% (Piores 1% dos dias):** -3.9958%
- **P5%:** -2.8006%
- **Q1 (25%):** -0.4229%
- **Mediana (50%):** -0.1267%
- **Q3 (75%):** -0.0274%
- **P95%:** 0.1078%
- **P99%:** 0.3165%

---

## 2. Impacto do Hard Fork Shanghai/Capella (Habilitação de Saques em 12/04/2023)

| Período | Dias | Depeg Médio (%) | Desvio Padrão (%) |
| :--- | :--- | :--- | :--- |
| **Pré-Shanghai** (Sem saques: Maio/22 a Abr/23) | 347 | -1.8218% | 1.3085% |
| **Pós-Shanghai** (Com saques: Abr/23 a Mai/26) | 1145 | -0.1159% | 0.2019% |

> **Resultado Econométrico Principal:** A habilitação dos saques na atualização Shanghai resultou em uma **redução de 84.6% na volatilidade do depeg**, estabilizando a paridade do derivativo stETH em torno de 1:1.

---

## 3. Dinâmica de Staking e Rendimento da Rede (Beacon Chain / ETH.STORE)

| Métrica | Início (Maio/2022) | Fim (Maio/2026) | Variação / Média |
| :--- | :--- | :--- | :--- |
| **Total em Staking (ETH)** | 11,625,590 | 39,255,940 | **+237.7% de crescimento** |
| **APR Médio da Rede** | - | - | **3.751% a.a.** |
| **Faixa de APR da Rede** | Mínimo: 2.536% a.a. | Máximo: 8.618% a.a. | Rendimento decrescente com aumento de validadores |
