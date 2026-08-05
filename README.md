# TCC — Código e Dados: Lido DAO & Liquid Staking no Ethereum

Repositório contendo exclusivamente os **scripts de coleta**, **datasets brutos em CSV**, **métricas estatísticas/econométricas**, **gráficos em alta resolução (300 DPI)** e **fichamentos bibliográficos** da pesquisa de TCC sobre **Lido DAO e Liquid Staking no Ethereum**.

---

## 📂 Estrutura do Repositório

```text
TCC_DEFI/
├── scripts_e_dados/
│   ├── scripts/                  # Scripts em Python para coleta, análise e gráficos
│   │   ├── 01_coleta_precos.py    # Coleta de preços ETH/USD e razão stETH/ETH (DefiLlama)
│   │   ├── 02_coleta_apr.py       # Coleta do APY/APR histórico do Lido e Solo Staking
│   │   ├── 03_coleta_tvl_lsd.py   # Coleta do TVL, Staking Ratio e Market Share dos LSDs
│   │   ├── 04_gerar_metricas.py   # Cálculo de estatísticas descritivas, testes t/F e HHI
│   │   ├── 05_gerar_graficos.py   # Geração das 8 figuras acadêmicas em alta resolução (300 DPI)
│   │   ├── coletar_todos.py       # Pipeline orquestradora completa (Execução única)
│   │   └── utils.py               # Módulo de utilidades e chamadas de API
│   │
│   ├── Dados/                     # Datasets brutos em formato CSV (2020 - 2026)
│   │   ├── depeg_steth_eth.csv
│   │   ├── preco_eth_usd.csv
│   │   ├── apr_lido_historico.csv
│   │   ├── apr_staking_direto_eth.csv
│   │   ├── tvl_lido.csv
│   │   ├── staking_ratio_eth.csv
│   │   ├── market_share_lsd.csv
│   │   └── market_share_lsd_snapshot.csv
│   │
│   ├── Metricas/                  # Tabelas estatísticas, JSON e Relatório Markdown
│   │   ├── relatorio_metricas_tcc.md
│   │   ├── resumo_metricas.json
│   │   ├── tabela_depeg_descritiva.csv
│   │   ├── tabela_pre_pos_shanghai.csv
│   │   ├── tabela_eventos_estresse.csv
│   │   └── tabela_rendimento_apr.csv
│   │
│   └── Graficos/                  # 8 Figuras em alta resolução (300 DPI) para a monografia
│       ├── fig01_depeg_historico_steth.png
│       ├── fig02_depeg_pre_pos_shanghai.png
│       ├── fig03_histograma_distribuicao_depeg.png
│       ├── fig04_rendimento_apr_lido_vs_solo.png
│       ├── fig05_evolucao_tvl_lido_vs_preco_eth.png
│       ├── fig06_market_share_historico_lsd.png
│       ├── fig07_dispersao_market_share_vs_depeg.png
│       └── fig08_indice_hhi_concentracao.png
│
└── fichamentos/                   # Fichamentos analíticos da literatura científica core
    ├── resumo_schar.md            # Schär (2021) - DeFi Stack & Risks
    ├── resumo_gogol_et_al.md      # Gogol et al. (2024) - LSPs Analysis
    ├── resumo_scharnowski_jahanshahloo.md # Scharnowski & Jahanshahloo (2025) - LSD Basis
    ├── resumo_xiong_et_al.md      # Xiong et al. (2024) - Leverage Staking
    ├── resumo_carre_gabriel.md    # Carré & Gabriel (2026) - General Equilibrium
    ├── resumo_nabben_defilippi.md # Nabben & De Filippi (2024) - Governance & Dual Gov
    ├── resumo_yang_et_al.md       # Yang et al. (2026) - Low Stake Attacks
    ├── resumo_cong_et_al.md       # Cong et al. (2025) - Staking Tokenomics
    ├── resumo_drissi_et_al.md     # Drissi et al. (2026) - Limits of Policy
    └── resumo_lim.md              # Lim (2026) - KelpDAO Exploit Case
```

---

## ⚡ Como Executar a Pipeline Completa

Os scripts utilizam o gerenciador moderno de pacotes Python `uv` com suporte a PEP 723 (gerenciamento automático de dependências isoladas).

Para executar toda a coleta de dados, cálculo de métricas e geração dos 8 gráficos com um único comando:

```bash
uv run scripts_e_dados/scripts/coletar_todos.py
```
