# Dicionário de Dados e Metadados Metodológicos — TCC Lido DAO & Liquid Staking

Este documento descreve detalhadamente a estrutura, metodologia de cálculo, fontes e definições de todas as tabelas e variáveis contidas no repositório de pesquisa sobre o protocolo **Lido DAO** e o derivativo **stETH** no ecossistema Ethereum.

---

## 📑 Sumário dos Datasets Disponíveis (`scripts_e_dados/Dados/`)

| Arquivo CSV | Descrição | Frequência | Período | Dimensões |
|---|---|---|---|---|
| **`dataset_master_tcc_2022_2026.csv`** | **Master Dataset Consolidado** com todas as variáveis unificadas via Full Outer Join temporal | Diária (UTC) | 05/05/2022 a 31/05/2026 | 1.488 linhas × 44 colunas |
| **`dados_precos_mercado.csv`** | Preços históricos spot de ETH e stETH, retornos logarítmicos, volatilidades móveis e paridade | Diária (UTC) | 01/04/2022 a 31/05/2026 | 1.522 linhas × 14 colunas |
| **`dados_rated_consenso.csv`** | Métricas da camada de consenso do Ethereum (PoS), APR direto da rede, curva de emissão e MEV | Diária (UTC) | 01/04/2022 a 31/05/2026 | 1.522 linhas × 11 colunas |
| **`dados_defillama_curve.csv`** | TVL do protocolo Lido, dominância no ecossistema DeFi e liquidez da pool Curve DEX stETH/ETH | Diária (UTC) | 05/05/2022 a 31/05/2026 | 1.488 linhas × 11 colunas |
| **`dados_mev_relay.csv`** | Dados de extração de MEV (Maximal Extractable Value) na camada de execução via relays | Diária (UTC) | 01/04/2022 a 31/05/2026 | 1.522 linhas × 7 colunas |

---

## 📊 Dicionário de Variáveis do Master Dataset (`dataset_master_tcc_2022_2026.csv`)

### 1. Bloco de Identificação Temporal e Regimes Institucionais

| Coluna | Tipo | Unidade | Descrição Metodológica |
|---|---|---|---|
| `Date` | String (`YYYY-MM-DD`) | Data UTC | Data de referência diária padronizada à meia-noite UTC (`00:00:00 UTC`). |
| `regime_ethereum` | Categórica | - | Regime institucional e técnico da rede Ethereum: <br>• `Pre-Merge` (Até 14/09/2022: Proof-of-Work + Beacon Chain isolada) <br>• `Post-Merge / Pre-Shapella` (15/09/2022 a 11/04/2023: PoS puro sem saques nativos) <br>• `Post-Shapella` (A partir de 12/04/2023: PoS com saques nativos 1:1 habilitados). |

---

### 2. Bloco de Preços de Mercado, Volatilidade e Paridade (Depeg / Basis)

| Coluna | Tipo | Unidade | Descrição Metodológica & Fórmula |
|---|---|---|---|
| `preco_eth_usd` | Float | USD ($) | Cotação spot de fechamento diário do Ether (ETH) em dólares americanos via Yahoo Finance / DefiLlama. |
| `preco_steth_usd` | Float | USD ($) | Cotação spot de fechamento diário do staked ETH (stETH) da Lido DAO em USD. |
| `preco_steth_eth` | Float | Ratio | Taxa de câmbio de mercado secundário entre stETH e ETH: <br>$$P_{\text{ratio}, t} = \frac{P_{stETH, t}}{P_{ETH, t}}$$ |
| `liquid_staking_basis` | Float | Spread | Desvio absoluto em relação à paridade teórica 1:1: <br>$$\text{Basis}_t = P_{\text{ratio}, t} - 1.0$$ |
| `depeg_pct` | Float | % | Desvio percentual da paridade (desconto se negativo, prêmio se positivo): <br>$$\text{Depeg}_t = \left(\frac{P_{stETH, t}}{P_{ETH, t}} - 1\right) \times 100$$ |
| `retorno_log_eth` | Float | - | Retorno logarítmico diário do ETH: <br>$$r_{ETH, t} = \ln\left(\frac{P_{ETH, t}}{P_{ETH, t-1}}\right)$$ |
| `retorno_log_steth` | Float | - | Retorno logarítmico diário do stETH: <br>$$r_{stETH, t} = \ln\left(\frac{P_{stETH, t}}{P_{stETH, t-1}}\right)$$ |
| `volatilidade_7d_anual_eth` | Float | % a.a. | Volatilidade histórica anualizada em janela móvel de 7 dias do ETH: <br>$$\sigma_{ETH, 7d} = \text{std}(r_{ETH, t-6:t}) \times \sqrt{365} \times 100$$ |
| `volatilidade_30d_anual_eth` | Float | % a.a. | Volatilidade histórica anualizada em janela móvel de 30 dias do ETH: <br>$$\sigma_{ETH, 30d} = \text{std}(r_{ETH, t-29:t}) \times \sqrt{365} \times 100$$ |
| `volatilidade_7d_anual_steth` | Float | % a.a. | Volatilidade histórica anualizada em janela móvel de 7 dias do stETH. |
| `volatilidade_30d_anual_steth` | Float | % a.a. | Volatilidade histórica anualizada em janela móvel de 30 dias do stETH. |

---

### 3. Bloco de Rendimentos, Spreads e Custo de Oportunidade da Governança

| Coluna | Tipo | Unidade | Descrição Metodológica & Fórmula |
|---|---|---|---|
| `apr_rede_direto_total_pct` | Float | % a.a. | Taxa anual nominal bruta estimada do Solo Staking direto (Consenso + Execução/MEV). |
| `apr_lido_liquido_pct` | Float | % a.a. | Taxa anual nominal recebida pelo investidor de stETH após dedução da taxa de protocolo da Lido DAO. |
| `delta_apr_pct` | Float | % a.a. | Spread anual de rendimento retido pelo protocolo (comissão de governança): <br>$$\Delta\text{APR}_t = \text{APR}_{\text{Rede Direto}, t} - \text{APR}_{\text{Lido Líquido}, t}$$ |
| `taxa_retencao_efetiva_pct` | Float | % | Proporção percentual efetiva retida pela Lido DAO (esperado ~10% contratual: 5% operadores de nó + 5% tesouraria): <br>$$\text{Taxa Retenção}_t = \frac{\Delta\text{APR}_t}{\text{APR}_{\text{Rede Direto}, t}} \times 100$$ |
| `custo_oportunidade_diario_pct` | Float | % ao dia | Custo de oportunidade diário incorrido pelo investidor por abrir mão do solo staking direto: <br>$$C_{\text{diário}, t} = \frac{\Delta\text{APR}_t}{365}$$ |
| `custo_oportunidade_acumulado_pct` | Float | % acum. | Custo de oportunidade acumulado ao longo do período amostral: <br>$$C_{\text{acum}, t} = \sum_{k=1}^t C_{\text{diário}, k}$$ |
| `apr_consenso_bruto_pct` | Float | % a.a. | Rendimento proveniente exclusivamente da emissão inflacionária da camada de consenso do Ethereum: <br>$$\text{APR}_{\text{Consenso}} \approx \frac{16632}{\sqrt{S_t}}$$ (onde $S_t$ é o total de ETH em staking na rede). |
| `taxa_mev_execucao_apr_pct` | Float | % a.a. | Rendimento anualizado derivado de gorjetas de prioridade (priority fees) e MEV na camada de execução. |
| `total_staked_eth_network` | Float | ETH | Quantidade total de Ether depositado no contrato de depósito da Beacon Chain. |
| `apy_lido_pct` | Float | % a.a. | Taxa efetiva anualizada composta (APY) divulgada pelo pool da Lido. |
| `apr_base_nominal_pct` | Float | % a.a. | Conversão estrita da taxa efetiva composta (APY) para taxa nominal (APR com capitalização diária $n=365$): <br>$$\text{APR} = 365 \times \left((1 + \text{APY})^{1/365} - 1\right)$$ |

---

### 4. Bloco de Liquidez DeFi, TVL e Pool DEX Curve stETH/ETH

| Coluna | Tipo | Unidade | Descrição Metodológica |
|---|---|---|---|
| `tvl_rede_ethereum_total_usd` | Float | USD ($) | Valor Total Bloqueado (Total Value Locked - TVL) agregado em todos os protocolos DeFi na rede Ethereum. |
| `tvl_lido_total_usd` | Float | USD ($) | TVL total sob custódia da Lido DAO em todas as redes atendidas (Ethereum, Polygon, etc.). |
| `tvl_lido_ethereum_usd` | Float | USD ($) | TVL da Lido DAO alocado exclusivamente em validadores na rede Ethereum. |
| `dominancia_lido_tvl_defi_pct` | Float | % | Participação de mercado do Lido no TVL de todo o ecossistema DeFi do Ethereum: <br>$$\text{Dominância}_t = \frac{\text{TVL Lido Ethereum}_t}{\text{TVL Total DeFi Ethereum}_t} \times 100$$ |
| `tvl_pool_curve_usd` | Float | USD ($) | Liquidez total alocada no pool de troca descentralizada (DEX) Curve stETH/ETH (`0xdc24316b9...`). |
| `apy_pool_curve_pct` | Float | % a.a. | Taxa APY base de taxas de negociação (trading fees) paga aos provedores de liquidez no pool Curve. |
| `tvl_yield_pool_usd` | Float | USD ($) | TVL reportado pelo endpoint de yields do DefiLlama para o contrato da pool. |

---

### 5. Bloco de Camada de Execução e MEV (Maximal Extractable Value)

| Coluna | Tipo | Unidade | Descrição Metodológica |
|---|---|---|---|
| `mev_valor_medio_bloco_eth` | Float | ETH | Recompensa média em ETH por bloco proposta por validadores via relays MEV-Boost. |
| `mev_total_diario_estimado_eth` | Float | ETH | Volume total diário de MEV extraído na rede (~7.150 blocos diários de 12s no Ethereum). |
| `mev_amostras_coletadas` | Inteiro | Qtd | Contagem de amostras empíricas processadas na janela diária. |
| `fonte_mev` | String | - | Identificador da fonte de dados de relays da camada de execução. |

---

### 6. Bloco de Variáveis Dummy de Estresse Sistêmico e Choques Exógenos

| Coluna | Tipo | Valores | Descrição do Evento |
|---|---|---|---|
| `evento_terra_luna` | Binária | `0` ou `1` | **Colapso do Ecossistema Terra/LUNA & UST** (08/05/2022 a 31/05/2022). Despejo massivo de stETH na Curve pela Celsius e Three Arrows Capital. |
| `evento_merge` | Binária | `0` ou `1` | **A Transição "The Merge"** (14/09/2022 a 18/09/2022). Unificação da Beacon Chain com a camada de execução (ativação do PoS). |
| `evento_ftx` | Binária | `0` ou `1` | **Falência da Exchange FTX & Alameda Research** (06/11/2022 a 20/11/2022). Choque de liquidez global nos mercados cripto. |
| `evento_shapella` | Binária | `0` ou `1` | **Upgrade Shanghai / Shapella** (12/04/2023 a 18/04/2023). Habilitação inédita de saques diretos no protocolo Ethereum. |

---

### 7. Bloco de Rastreabilidade e Auditoria de Dados

| Coluna | Tipo | Descrição |
|---|---|---|
| `fonte_preco_eth` | String | Origem do preço do ETH (`yfinance_ETH-USD` / `defillama_coins`). |
| `fonte_preco_steth` | String | Origem do preço do stETH (`yfinance_STETH-USD` / `defillama_coins`). |
| `fonte_consenso` | String | Método de cálculo da taxa de consenso (`beacon_formula_16632_sqrt_S`). |
| `qualidade_dado` | String | Validação de consistência do registro temporal (`modelo_teorico_e_real`). |

---

## 📐 Fórmulas Matemáticas e Métodos de Cálculo

### 1. Paridade de Mercado e Depeg (Basis)
$$\text{Preço Ratio}_t = \frac{P_{stETH, t}}{P_{ETH, t}}$$
$$\text{Depeg (\%)}_t = \left(\frac{P_{stETH, t}}{P_{ETH, t}} - 1\right) \times 100$$

### 2. Conversão da Taxa Composta (APY) para Taxa Nominal (APR)
$$\text{APR}_t = 365 \times \left((1 + \text{APY}_t)^{1/365} - 1\right)$$

### 3. Curva Teórica de Emissão da Beacon Chain
$$\text{APR}_{\text{Consenso}, t} = \frac{C}{\sqrt{S_t}} = \frac{16632}{\sqrt{S_t}}$$
*onde $S_t$ é o total de ETH depositado na camada de consenso.*

### 4. Modelo de Retenção Contratual da Lido DAO

$$\text{APR}_{\text{Direto}, t} = \frac{\text{APR}_{\text{Lido Líquido}, t}}{1 - \tau} = \frac{\text{APR}_{\text{Lido Líquido}, t}}{0{,}90}$$
$$\Delta\text{APR}_t = \text{APR}_{\text{Direto}, t} - \text{APR}_{\text{Lido Líquido}, t} = \tau \cdot \text{APR}_{\text{Direto}, t}$$
*onde $\tau = 0,10$ (10% de comissão retida pelo protocolo).*


### 5. Custo de Oportunidade Acumulado
$$C_{\text{acum}, t} = \sum_{k=1}^t \left(\frac{\Delta\text{APR}_k}{365}\right)$$
