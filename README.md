# TCC — Código, Dados e Documentação: Lido DAO & Liquid Staking no Ethereum

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maths0007/TCC_DEFI/blob/master/notebook_tcc_lido_defi.ipynb)

Repositório oficial organizado para o trabalho de conclusão de curso (TCC) sobre o protocolo **Lido DAO** e o token derivativo **stETH** no ecossistema Ethereum.

---

## 📂 Estrutura Modular Limpa do Repositório

```text
TCC_DEFI/
├── notebook_tcc_lido_defi.ipynb  # Notebook interativo para Google Colab / Jupyter
├── requirements.txt              # Dependências Python (pip / venv)
├── .env.example                  # Modelo de variáveis de ambiente
│
├── apresentacao/                 # Apresentação do TCC (PPTX, gerador Python e Slides Web)
│   ├── Apresentacao_TCC_Matheus.pptx
│   ├── gerar_pptx.py
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── artigos_cientificos/          # Biblioteca de artigos da literatura organizados por relevância
│   ├── selecionados/             # Artigos primários citados diretamente no TCC (PDFs)
│   ├── referencia/               # Artigos de fundamentação teórica mantidos (PDFs)
│   ├── baixados/                 # Artigos em fase de leitura (PDFs)
│   └── descartados/              # Artigos descartados no rastreamento (PDFs)
│
├── fichamentos/                  # Fichamentos analíticos em Markdown dos artigos
│
├── texto_tcc/                    # Minuta da monografia e arquivos de texto ABNT
│
├── scripts_e_dados/              # PIPELINE ATUAL EM FUNCIONAMENTO (2022 - 2026)
│   ├── scripts/                  # Scripts Python da pipeline master ativa
│   │   ├── 01_coleta_precos.py          # Preços ETH/USD, retornos log e volatilidade
│   │   ├── 02_coleta_rated_network.py   # Métricas da camada de consenso (Rated Network)
│   │   ├── 02b_coleta_mev_relay.py      # MEV e dados de relays da camada de consenso
│   │   ├── 03_coleta_defillama_curve.py # TVL, Yields e Reservas DEX (Curve & DefiLlama)
│   │   ├── 04_consolidar_dataset.py     # Consolidação do Master Dataset (2022-2026)
│   │   ├── 05_gerar_graficos_tcc.py     # Renderização de gráficos acadêmicos em 300 DPI
│   │   ├── executar_pipeline.py         # Orquestrador mestre da pipeline
│   │   ├── formatar_dataset.py          # Padronizador de esquema
│   │   ├── validar_dados_tcc.py         # Validador de integridade estatística
│   │   └── utils.py                     # Utilitários e helpers de API
│   │
│   ├── Dados/                    # Datasets do Master Dataset Ativo (CSV)
│   │   ├── dataset_master_tcc_2022_2026.csv
│   │   ├── dados_defillama_curve.csv
│   │   ├── dados_mev_relay.csv
│   │   ├── dados_precos_mercado.csv
│   │   └── dados_rated_consenso.csv
│   │
│   ├── Metricas/                 # Relatórios econométricos e tabelas consolidadas
│   │   ├── relatorio_metricas_tcc.md
│   │   ├── resumo_metricas.json
    │   ├── tabela_metricas_consolidadas_tcc.csv
    │   ├── tabela_depeg_descritiva.csv
    │   ├── tabela_pre_pos_shanghai.csv
    │   ├── tabela_eventos_estresse.csv
    │   └── tabela_rendimento_apr.csv
│   │
│   └── Graficos/                 # Figuras em alta resolução (300 DPI) para a monografia
│       ├── fig01_depeg_historico_steth.png
│       ├── fig02_depeg_pre_pos_shanghai.png
│       ├── fig03_histograma_distribuicao_depeg.png
│       ├── fig04_rendimento_apr_lido_vs_solo.png
│       ├── fig05_evolucao_tvl_lido_vs_preco_eth.png
│       ├── fig06_market_share_historico_lsd.png
│       ├── fig07_dispersao_market_share_vs_depeg.png
│       └── fig08_indice_hhi_concentracao.png
│
└── arquivo_obsoleto/             # PASTA ÚNICA PARA SCRIPTS E TABELAS LEGADAS/OBSOLETAS
    ├── scripts_legados/          # Versões anteriores de scripts
    ├── dados_legados/            # CSVs antigos do recorte de 2020
    └── rascunhos_texto/          # Rascunhos antigos de documentos
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
