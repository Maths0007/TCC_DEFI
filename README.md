# TCC — Código e Dados: Lido DAO & Liquid Staking no Ethereum

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maths0007/TCC_DEFI/blob/master/notebook_tcc_lido_defi.ipynb)

Repositório oficial contendo os **scripts de coleta de dados**, **datasets brutos em CSV**, **métricas estatísticas/econométricas**, **gráficos acadêmicos (300 DPI)** e **Jupyter Notebook interativo para Google Colab** para a pesquisa de TCC sobre o protocolo **Lido DAO** e o token derivativo **stETH** no ecossistema Ethereum.

---

## ⚡ Abrir e Rodar no Google Colab com 1 Clique

Clique no botão abaixo para abrir o notebook interativo diretamente no **Google Colab** (não exige instalação de nada na sua máquina):

👉 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maths0007/TCC_DEFI/blob/master/notebook_tcc_lido_defi.ipynb)

---

## 📂 Estrutura do Repositório

```text
TCC_DEFI/
├── notebook_tcc_lido_defi.ipynb  # Notebook interativo para Google Colab / Jupyter
└── scripts_e_dados/
    ├── scripts/                  # Scripts em Python para coleta, análise e gráficos
    │   ├── 01_coleta_precos.py    # Coleta de preços ETH/USD e razão stETH/ETH (DefiLlama)
    │   ├── 02_coleta_apr.py       # Coleta do APY/APR histórico do Lido e Solo Staking
    │   ├── 03_coleta_tvl_lsd.py   # Coleta do TVL, Staking Ratio e Market Share dos LSDs
    │   ├── 04_gerar_metricas.py   # Cálculo de estatísticas descritivas, testes t/F e HHI
    │   ├── 05_gerar_graficos.py   # Geração das 8 figuras acadêmicas em alta resolução (300 DPI)
    │   ├── coletar_todos.py       # Pipeline orquestradora completa (Execução única)
    │   └── utils.py               # Módulo de utilidades e chamadas de API
    │
    ├── Dados/                     # Datasets brutos em formato CSV (2020 - 2026)
    │   ├── depeg_steth_eth.csv
    │   ├── preco_eth_usd.csv
    │   ├── apr_lido_historico.csv
    │   ├── apr_staking_direto_eth.csv
    │   ├── tvl_lido.csv
    │   ├── staking_ratio_eth.csv
    │   ├── market_share_lsd.csv
    │   └── market_share_lsd_snapshot.csv
    │
    ├── Metricas/                  # Tabelas estatísticas, JSON e Relatório Markdown
    │   ├── relatorio_metricas_tcc.md
    │   ├── resumo_metricas.json
    │   ├── tabela_depeg_descritiva.csv
    │   ├── tabela_pre_pos_shanghai.csv
    │   ├── tabela_eventos_estresse.csv
    │   └── tabela_rendimento_apr.csv
    │
    └── Graficos/                  # 8 Figuras em alta resolução (300 DPI) para a monografia
        ├── fig01_depeg_historico_steth.png
        ├── fig02_depeg_pre_pos_shanghai.png
        ├── fig03_histograma_distribuicao_depeg.png
        ├── fig04_rendimento_apr_lido_vs_solo.png
        ├── fig05_evolucao_tvl_lido_vs_preco_eth.png
        ├── fig06_market_share_historico_lsd.png
        ├── fig07_dispersao_market_share_vs_depeg.png
        └── fig08_indice_hhi_concentracao.png
```

---

## 📖 Tutorial Passo a Passo: Como Rodar no Google Colab ou Jupyter

### Opção A: Executar no Google Colab (Na Nuvem, Sem Instalar Nada)
1. Clique no selo azul **[Open In Colab]** no topo desta página.
2. No menu superior do Colab, clique em **Ambiente de execução > Executar tudo** (ou pressione `Ctrl + F9`).
3. O Colab irá baixar os pacotes necessários, consultar as APIs on-chain e exibir todos os gráficos e métricas na tela.

---

### Opção B: Executar Localmente via Jupyter Notebook ou VS Code
1. Clone este repositório:
   ```bash
   git clone https://github.com/Maths0007/TCC_DEFI.git
   cd TCC_DEFI
   ```
2. Abra o arquivo `notebook_tcc_lido_defi.ipynb` no VS Code, Jupyter Lab ou Jupyter Notebook.
3. Clique em **Run All** (Executar Tudo).

---

### Opção C: Executar via Terminal com `uv`
Para rodar a pipeline automatizada completa direto no terminal de comando:
```bash
uv run scripts_e_dados/scripts/coletar_todos.py
```
