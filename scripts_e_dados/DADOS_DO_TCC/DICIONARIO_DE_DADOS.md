# Dicionário de Dados — TCC Lido DAO & Liquid Staking

Este documento descreve as variáveis contidas na pasta **`DADOS_DO_TCC/`**, seu significado econômico, unidade de medida e fonte original.

---

## 📁 1. `dataset_consolidado_tcc.csv`
Arquivo principal para a pesquisa de TCC, unificando as métricas econômicas e financeiras diárias de **01/05/2022 a 31/05/2026** (1.492 observações diárias).

| Nome da Coluna | Tipo | Unidade | Descrição / Fórmula | Fonte |
| :--- | :--- | :--- | :--- | :--- |
| **`data`** | Data | AAAA-MM-DD | Data civil da observação em fuso UTC | - |
| **`total_eth_staked`** | Numérico | ETH | Saldo efetivo total de Ether depositado em validadores ativos na Beacon Chain | Beaconcha.in |
| **`apr_rede_ethstore_pct`** | Numérico | % a.a. | Taxa anualizada de rendimento da rede Ethereum (ETH.STORE) em janelas de 24h | Beaconcha.in ETH.STORE |
| **`preco_eth_usd`** | Numérico | USD ($) | Preço diário de fechamento do Ethereum em dólares | Yahoo Finance (`ETH-USD`) |
| **`preco_steth_usd`** | Numérico | USD ($) | Preço diário de fechamento do stETH (Lido) em dólares | Yahoo Finance (`STETH-USD`) |
| **`razao_steth_eth`** | Numérico | Ratio | Razão de preço $\frac{\text{stETH}}{\text{ETH}}$. Paridade perfeita = 1.000000 | Derivado (Yahoo) |
| **`depeg_pct`** | Numérico | % | Desvio percentual da paridade: $(\frac{\text{stETH}}{\text{ETH}} - 1) \times 100$ | Derivado (Yahoo) |
| **`retorno_log_eth`** | Numérico | Decimal | Retorno logarítmico diário: $\ln(P_t / P_{t-1})$ do ETH | Derivado |
| **`retorno_log_steth`** | Numérico | Decimal | Retorno logarítmico diário: $\ln(P_t / P_{t-1})$ do stETH | Derivado |
| **`volatilidade_anual_eth_30d`** | Numérico | % a.a. | Volatilidade móvel anualizada (30 dias) dos retornos do ETH: $\sigma_{30d} \times \sqrt{365} \times 100$ | Derivado |
| **`volatilidade_anual_steth_30d`** | Numérico | % a.a. | Volatilidade móvel anualizada (30 dias) dos retornos do stETH: $\sigma_{30d} \times \sqrt{365} \times 100$ | Derivado |

---

## 📁 2. Arquivos Temáticos Especializados

1. **`dados_precos_e_depeg.csv`**:
   Contém especificamente as séries de preços de mercado, razão stETH/ETH, depeg percentual, retornos e volatilidades.
2. **`dados_staking_e_apr.csv`**:
   Contém as métricas de segurança on-chain e rendimento: total de ETH em staking, APR da rede, recompensas diárias pagas aos validadores e saldo efetivo elegível.
3. **`tecnico_auditoria/`**:
   Contém o arquivo com todas as 36 colunas brutas, URLs, timestamps em milissegundos e relatórios de auditoria matemática (`auditoria_tcc.json`).
