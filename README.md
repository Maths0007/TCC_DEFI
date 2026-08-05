# TCC — Análise Empírica do Lido DAO e Liquid Staking no Ethereum

Repositório oficial do Trabalho de Conclusão de Curso (TCC) sobre **Finanças Descentralizadas (DeFi)**, focado na análise econométrica, de riscos e de governança do protocolo **Lido DAO** e do token derivativo **stETH**.

---

## 📌 Resumo da Pesquisa

O trabalho examina o ecossistema de *Liquid Staking Derivatives* (LSD) e *Liquid Restaking Tokens* (LRT) na rede Ethereum (Proof-of-Stake), investigando:
1. **Desempenho Financeiro e Yield:** Comparação entre o rendimento do Lido stETH e o *Solo Staking* direto, isolando a comissão de 10% cobrada pelo Lido DAO.
2. **Estabilidade do Peg e Risco de Descolamento (*Basis Risk*):** Análise econométrica e estatística do *depeg* do stETH/ETH (2020-2026), testando o impacto de eventos de estresse sistêmico (Terra/LUNA, FTX, KelpDAO) e o efeito mitigador da habilitação de saques nativos no **Upgrade Shanghai/Capella**.
3. **Concentração de Mercado e Governança:** Avaliação do risco de monopólio/oligopólio no consenso do Ethereum através do índice Herfindahl-Hirschman (HHI) e da relação empírica entre *Market Share* do Lido e prêmio de risco no mercado secundário.

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
├── fichamentos/                   # Fichamentos analíticos da literatura científica core
│   ├── resumo_schar.md            # Schär (2021) - DeFi Stack & Risks
│   ├── resumo_gogol_et_al.md      # Gogol et al. (2024) - LSPs Analysis
│   ├── resumo_scharnowski_jahanshahloo.md # Scharnowski & Jahanshahloo (2025) - LSD Basis
│   ├── resumo_xiong_et_al.md      # Xiong et al. (2024) - Leverage Staking
│   ├── resumo_carre_gabriel.md    # Carré & Gabriel (2026) - General Equilibrium
│   ├── resumo_nabben_defilippi.md # Nabben & De Filippi (2024) - Governance & Dual Gov
│   ├── resumo_yang_et_al.md       # Yang et al. (2026) - Low Stake Attacks
│   ├── resumo_cong_et_al.md       # Cong et al. (2025) - Staking Tokenomics
│   ├── resumo_drissi_et_al.md     # Drissi et al. (2026) - Limits of Policy
│   └── resumo_lim.md              # Lim (2026) - KelpDAO Exploit Case
│
└── texto_tcc/                     # Manuscritos da monografia e arquivos ABNT
```

---

## ⚡ Como Executar a Pipeline Completa

Os scripts utilizam o gerenciador moderno de pacotes Python `uv` com suporte a PEP 723 (gerenciamento automático de dependências isoladas).

Para executar toda a coleta de dados, cálculo de métricas e geração dos 8 gráficos com um único comando:

```bash
uv run scripts_e_dados/scripts/coletar_todos.py
```

---

## 📊 Resumo dos Achados Empíricos

* **Depeg Médio:** `-0,43%` no período 2020-2026.
* **Pior Desconto Histórico:** `-21,80%` durante o crash do ecossistema Terra/LUNA (Maio/2022).
* **Efeito Shanghai (Saques Nativos):** A volatilidade do depeg sofreu uma **redução de ~70%+** pós-Upgrade Shanghai (12/04/2023), estabilizando a arbitragem 1:1.
* **Comissão da Lido DAO:** A taxa de 10% cobrada pelo protocolo resulta em um *spread* médio de `0,386% a.a.` em relação ao *Solo Staking* direto.
* **Dominância da Lido:** O Lido detém atualmente **~53,8%** do mercado de *Liquid Staking* no Ethereum, operando em um mercado de alta concentração (Índice HHI > 2.500).
