# TCC — Código e Dados: Lido DAO & Liquid Staking no Ethereum

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maths0007/TCC_DEFI/blob/master/notebook_tcc_lido_defi.ipynb)

Repositório oficial contendo os **scripts de coleta de dados**, **datasets brutos em CSV**, **métricas estatísticas/econométricas**, **gráficos acadêmicos (300 DPI)** e **Jupyter Notebook interativo para Google Colab** para a pesquisa de TCC sobre o protocolo **Lido DAO** e o token derivativo **stETH** no ecossistema Ethereum.

---

## 📂 Estrutura do Repositório

```text
TCC_DEFI/
├── notebook_tcc_lido_defi.ipynb  # Notebook interativo para Google Colab / Jupyter
├── requirements.txt              # Arquivo de dependências Python para venv / pip
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

## 📖 Tutorial Passo a Passo: Como Rodar no Seu Ambiente Virtual (`venv`)

Este é o método tradicional para executar o projeto no seu computador utilizando o ambiente virtual Python (`venv`) e o gerenciador `pip`.

### 💻 1. No Windows (PowerShell)

1. **Abra o PowerShell** na pasta do projeto e crie o ambiente virtual:
   ```powershell
   python -m venv .venv
   ```

2. **Ative o ambiente virtual:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   *(Caso apareça aviso de permissão de execução de scripts, rode antes: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

3. **Instale as dependências:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Execute a pipeline completa (Coleta + Métricas + Gráficos 300 DPI):**
   ```powershell
   python scripts_e_dados/scripts/coletar_todos.py
   ```

---

### 🐧 / 🍎 2. No Linux ou macOS (Terminal)

1. **Abra o Terminal** na pasta do projeto e crie o ambiente virtual:
   ```bash
   python3 -m venv .venv
   ```

2. **Ative o ambiente virtual:**
   ```bash
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a pipeline completa:**
   ```bash
   python scripts_e_dados/scripts/coletar_todos.py
   ```

---

## ⚡ Outras Formas de Execução

### Opção B: Executar no Google Colab (Na Nuvem, Sem Instalar Nada)
Clique no botão abaixo para rodar o notebook interativo na nuvem do Google Colab com 1 clique:

👉 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maths0007/TCC_DEFI/blob/master/notebook_tcc_lido_defi.ipynb)

---

### Opção C: Executar com `uv` (Execução Direta sem venv Manual)
Se preferir usar o gerenciador `uv`:
```bash
uv run scripts_e_dados/scripts/coletar_todos.py
```

---

## ⚙️ Executando Scripts Individuais no Ambiente Virtual

Com o ambiente virtual ativado (`.venv`), você também pode executar cada script isoladamente:

```bash
# 1. Coletar preços de ETH/USD e razões stETH/ETH (Depeg)
python scripts_e_dados/scripts/01_coleta_precos.py

# 2. Coletar histórico de APR/APY do Lido e Solo Staking
python scripts_e_dados/scripts/02_coleta_apr.py

# 3. Coletar TVL, Staking Ratio e Market Share dos LSDs/LRTs
python scripts_e_dados/scripts/03_coleta_tvl_lsd.py

# 4. Calcular estatísticas descritivas, testes t/F e HHI
python scripts_e_dados/scripts/04_gerar_metricas.py

# 5. Gerar os 8 gráficos acadêmicos em alta resolução (300 DPI)
python scripts_e_dados/scripts/05_gerar_graficos.py
```
