# TCC — Código e Dados: Lido DAO & Liquid Staking no Ethereum

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maths0007/TCC_DEFI/blob/master/notebook_tcc_lido_defi.ipynb)

Repositório oficial contendo a **pipeline auditada de dados**, **datasets organizados e intuitivos**, **fontes metodológicas com hashes SHA-256**, **métricas econométricas atualizadas**, **gráficos acadêmicos** e **Jupyter Notebook interativo para Google Colab** para a pesquisa de TCC sobre o protocolo **Lido DAO** e o token derivativo **stETH** no ecossistema Ethereum.

---

## 📂 Estrutura Intuitiva dos Dados e Scripts

```text
TCC_DEFI/
├── executar_pipeline.py          # Orquestrador oficial da pipeline
├── testar_pipeline.py            # Bateria de testes de integridade e completude
├── comum_tcc.py                  # Calendário (Maio/22 a Maio/26), caminhos e validação
├── requirements.txt              # Dependências Python
├── notebook_tcc_lido_defi.ipynb  # Notebook interativo para Google Colab / Jupyter
├── fontes/                       # Dados brutos das fontes, metodologia e manifesto
│   ├── manifesto.json            # Hashes SHA-256 de todas as fontes
│   ├── apr/                      # HTML, extrator e metodologia ETH.STORE
│   └── staking/                  # HTML, extrator e metodologia Beaconcha.in Staked Ether
│
└── scripts_e_dados/
    ├── DADOS_DO_TCC/             # 🌟 PASTA PRINCIPAL DE DADOS (LIMPOS E INTUITIVOS)
    │   ├── dataset_consolidado_tcc.csv # Dataset principal com 11 variáveis econômicas prontas para análise
    │   ├── dados_precos_e_depeg.csv    # Série temática: ETH, stETH, razão e métrica de Depeg
    │   ├── dados_staking_e_apr.csv     # Série temática: Total em Staking, APR ETH.STORE e Recompensas
    │   ├── DICIONARIO_DE_DADOS.md      # Dicionário com nomes, fórmulas e unidades de cada variável
    │   └── tecnico_auditoria/          # Dados brutos com 36 colunas técnicas e metadados de auditoria
    │       ├── dataset_completo_com_metadados.csv
    │       ├── auditoria_tcc.json
    │       └── execucao.json
    │
    ├── Graficos/                 # Figuras em alta resolução geradas pela pipeline
    │   ├── mercado_steth.png     # Série histórica de Preços (ETH/stETH) e Depeg (%)
    │   └── staking_apr_rede.png  # Série de Saldo em Staking e Rendimento ETH.STORE
    │
    ├── Metricas/                 # Relatórios estatísticos e tabelas econométricas
    │   ├── relatorio_metricas_atualizado.md # Relatório formatado com testes Pré vs Pós-Shanghai
    │   └── resumo_metricas_atualizado.json  # Resumo em JSON para gráficos e tabelas
    │
    └── scripts/                  # Scripts em Python organizados
        ├── 01_coleta_precos.py
        ├── 02_coleta_rated_network.py
        ├── 02a_coleta_staking_rewards.py
        ├── 03_coleta_defillama_curve.py
        ├── 04_consolidar_dataset.py
        ├── 05_gerar_graficos_tcc.py
        ├── executar_pipeline.py
        └── organizar_dados_intuitivos.py
```

---

## 📊 Principais Variáveis (`DADOS_DO_TCC/dataset_consolidado_tcc.csv`)

| Coluna | Unidade | Descrição |
| :--- | :--- | :--- |
| `data` | AAAA-MM-DD | Data civil UTC (01/05/2022 a 31/05/2026 — 1.492 observações) |
| `total_eth_staked` | ETH | Saldo efetivo em staking na rede (Beaconcha.in) |
| `apr_rede_ethstore_pct` | % a.a. | Rendimento da rede Ethereum (ETH.STORE) em janelas de 24h |
| `preco_eth_usd` | USD ($) | Preço diário de fechamento do ETH (Yahoo Finance) |
| `preco_steth_usd` | USD ($) | Preço diário de fechamento do stETH (Yahoo Finance) |
| `razao_steth_eth` | Ratio | Razão de preço $\frac{\text{stETH}}{\text{ETH}}$ (paridade teórica = 1.000000) |
| `depeg_pct` | % | Desvio percentual: $(\frac{\text{stETH}}{\text{ETH}} - 1) \times 100$ |
| `retorno_log_eth / steth` | Decimal | Retornos logarítmicos diários $\ln(P_t / P_{t-1})$ |
| `volatilidade_anual_..._30d` | % a.a. | Volatilidade móvel anualizada (janela de 30 dias) |

---

## 🚀 Como Executar

### 1. Testar Integridade da Pipeline
```powershell
python testar_pipeline.py
```

### 2. Executar a Pipeline Completa
```powershell
python executar_pipeline.py --somente-beaconchain --offline
```

### 3. Reorganizar os Dados Intuitivos e Recalcular Métricas
```powershell
python scripts_e_dados/scripts/organizar_dados_intuitivos.py
```
