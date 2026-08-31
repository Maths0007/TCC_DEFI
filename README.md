# TCC — Código, Dados e Documentação: Lido DAO & Liquid Staking no Ethereum

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maths0007/TCC_DEFI/blob/master/notebook_tcc_lido_defi.ipynb)

Repositório oficial organizado para o trabalho de conclusão de curso (TCC) sobre o protocolo **Lido DAO** e o token derivativo **stETH** no ecossistema Ethereum.

---

## 📂 Estrutura Reorganizada do Repositório

```text
TCC_DEFI/
├── notebook_tcc_lido_defi.ipynb  # Notebook interativo para Google Colab / Jupyter
├── requirements.txt              # Arquivo de dependências Python para venv / pip
├── .env.example                  # Modelo de variáveis de ambiente
│
├── apresentacao/                 # Apresentação do TCC (PPTX, gerador Python e Slides Web)
│   ├── Apresentacao_TCC_Matheus.pptx
│   ├── gerar_pptx.py
│   └── apresentacao_web/
│
├── artigos_cientificos/          # Biblioteca de artigos da literatura organizados por status
│   ├── artigos_selecionados_tcc/ # Artigos com citação direta no texto do TCC
│   ├── artigos_selecionados/
│   ├── artigos_manter/
│   ├── artigos_novos/
│   ├── artigos_baixados/
│   └── artigos_descartados/
│
├── fichamentos/                  # Fichamentos analíticos da literatura acadêmica
│
├── texto_tcc/                    # Minuta da monografia, capítulos e documentos de texto
│
└── scripts_e_dados/              # Toda a engenharia de dados, scripts e resultados
    ├── scripts/                  # Scripts Python de coleta, consolidação e visualização
    │   ├── 01_coleta_precos.py    # Coleta de preços ETH/USD e razão stETH/ETH (DefiLlama / yfinance)
    │   ├── 02_coleta_rated_network.py # Métricas da camada de consenso (Rated Network)
    │   ├── 02_coleta_apr.py       # Histórico de APY/APR Lido e Solo Staking
    │   ├── 03_coleta_defillama_curve.py # TVL, Yields e Reservas DEX (Curve & DefiLlama)
    │   ├── 03_coleta_tvl_lsd.py   # Staking Ratio e Market Share dos LSDs/LRTs
    │   ├── 04_consolidar_dataset.py # Consolidação do Master Dataset (2022-2026)
    │   ├── 04_gerar_metricas.py   # Estatísticas descritivas, testes econométricos (t/F) e HHI
    │   ├── 05_gerar_graficos_tcc.py # Renderização de gráficos acadêmicos em 300 DPI
    │   ├── 05_gerar_graficos.py   # Figuras 01 a 08 em alta resolução (300 DPI)
    │   ├── executar_pipeline.py   # Orquestrador mestre da pipeline quantitativa
    │   ├── coletar_todos.py       # Pipeline auxiliar de coleta completa
    │   ├── formatar_dataset.py    # Padronizador de esquema e datas
    │   ├── validar_dados_tcc.py   # Validador de integridade estatística
    │   └── utils.py               # Utilitários e helpers de API
    │
    ├── Dados/                     # Datasets brutos e consolidados em formato CSV
    │   ├── dataset_master_tcc_2022_2026.csv
    │   ├── dados_defillama_curve.csv
    │   ├── dados_precos_mercado.csv
    │   ├── dados_rated_consenso.csv
    │   ├── depeg_steth_eth.csv
    │   ├── preco_eth_usd.csv
    │   ├── apr_lido_historico.csv
    │   ├── apr_staking_direto_eth.csv
    │   ├── tvl_lido.csv
    │   ├── staking_ratio_eth.csv
    │   └── market_share_lsd.csv
    │
    ├── Metricas/                  # Relatório econométrico, JSON e tabelas organizadas
    │   ├── relatorio_metricas_tcc.md
    │   ├── resumo_metricas.json
    │   ├── tabela_metricas_consolidadas_tcc.csv
    │   ├── tabela_depeg_descritiva.csv
    │   ├── tabela_pre_pos_shanghai.csv
    │   ├── tabela_eventos_estresse.csv
    │   └── tabela_rendimento_apr.csv
    │
    └── Graficos/                  # Figuras em alta resolução (300 DPI) para a monografia
        ├── fig01_depeg_historico_steth.png
        ├── fig02_depeg_pre_pos_shanghai.png
        ├── fig03_histograma_distribuicao_depeg.png
        ├── fig04_rendimento_apr_lido_vs_solo.png
        ├── fig05_evolucao_tvl_lido_vs_preco_eth.png
        ├── fig06_market_share_historico_lsd.png
        ├── fig07_dispersao_market_share_vs_depeg.png
        ├── fig08_indice_hhi_concentracao.png
        ├── grafico_01_paridade_depeg_2022_2026.png
        └── grafico_02_comparativo_apr_retornos.png
```

---

## 📖 Como Executar o Projeto

### Opção A: Executar via Ambiente Virtual (`venv` + `pip`)

```powershell
# 1. Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

# 2. Executar o orquestrador da pipeline quantitativa
python scripts_e_dados/scripts/executar_pipeline.py
```

### Opção B: Executar no Google Colab (1 Clique)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maths0007/TCC_DEFI/blob/master/notebook_tcc_lido_defi.ipynb)
