# TCC — Código e Dados: Lido DAO & Liquid Staking no Ethereum

Repositório oficial contendo exclusivamente os **scripts de coleta de dados**, **datasets brutos em CSV**, **métricas estatísticas/econométricas** e **gráficos acadêmicos em alta resolução (300 DPI)** para a pesquisa de TCC sobre o protocolo **Lido DAO** e o token derivativo **stETH** no ecossistema Ethereum.

---

## 📂 Estrutura do Repositório

```text
TCC_DEFI/
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

## 📖 Tutorial Passo a Passo: Como Rodar o Projeto

Siga este tutorial prático para clonar o repositório, executar a pipeline de dados e gerar todas as tabelas e gráficos no seu computador.

### 📋 1. Pré-requisitos
Antes de começar, certifique-se de ter instalado:
* **Python** (versão 3.11 ou superior): [Download Python](https://www.python.org/downloads/)
* **Git**: [Download Git](https://git-scm.com/downloads)
* **uv** (Gerenciador moderno de pacotes Python):
  ```bash
  # No Windows (PowerShell):
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

  # No Linux / macOS:
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

---

### 📥 2. Clonar o Repositório
Abra o terminal (ou Prompt de Comando / PowerShell) e rode:

```bash
git clone https://github.com/Maths0007/TCC_DEFI.git
cd TCC_DEFI
```

---

### 🚀 3. Execução Automatizada (Recomendado)

Você não precisa instalar dependências manualmente em ambientes virtuais (`pip install`). Os scripts utilizam o padrão **PEP 723**, permitindo que o `uv` baixe e isole as dependências automaticamente (`pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`, `requests`).

Para rodar a **pipeline completa** (coleta de dados + cálculo de métricas + geração de 8 gráficos 300 DPI) em um único comando:

```bash
uv run scripts_e_dados/scripts/coletar_todos.py
```

---

### ⚙️ 4. Execução Etapa por Etapa (Opcional)

Se preferir executar cada etapa separadamente:

#### Etapa A: Coletar os Dados Brutos (APIs da DefiLlama)
```bash
# Coletar preços de ETH/USD e razões stETH/ETH (Depeg)
uv run scripts_e_dados/scripts/01_coleta_precos.py

# Coletar histórico de APR/APY do Lido e Solo Staking
uv run scripts_e_dados/scripts/02_coleta_apr.py

# Coletar TVL, Staking Ratio e Market Share dos protocolos LSD/LRT
uv run scripts_e_dados/scripts/03_coleta_tvl_lsd.py
```

#### Etapa B: Calcular Métricas Estatísticas e Econométricas
```bash
uv run scripts_e_dados/scripts/04_gerar_metricas.py
```
*Gera os arquivos de resultados descritivos, testes t/F (Pré vs. Pós Shanghai) e JSON consolidado em `scripts_e_dados/Metricas/`.*

#### Etapa C: Gerar os 8 Gráficos Acadêmicos (300 DPI)
```bash
uv run scripts_e_dados/scripts/05_gerar_graficos.py
```
*Gera todas as 8 figuras em formato PNG de alta resolução salvas em `scripts_e_dados/Graficos/`.*

---

### 📊 5. Onde Encontrar os Resultados Gerados

Após rodar os comandos acima, os arquivos finais estarão disponíveis nas seguintes pastas:

1. **CSVs com Dados Históricos (2020 - 2026):**
   * `scripts_e_dados/Dados/depeg_steth_eth.csv` — Cotação stETH/ETH e porcentagem de depeg.
   * `scripts_e_dados/Dados/preco_eth_usd.csv` — Série temporal de preço do Ethereum.
   * `scripts_e_dados/Dados/apr_lido_historico.csv` — Rendimento percentual do stETH.
   * `scripts_e_dados/Dados/apr_staking_direto_eth.csv` — Rendimento do Solo Staking e spread de taxa da DAO (10%).
   * `scripts_e_dados/Dados/market_share_lsd.csv` — Participação de mercado histórica dos competidores.

2. **Relatórios e Métricas Estatísticas:**
   * `scripts_e_dados/Metricas/relatorio_metricas_tcc.md` — Relatório formatado em Markdown pronto para cópia/leitura.
   * `scripts_e_dados/Metricas/tabela_pre_pos_shanghai.csv` — Comparativo de volatilidade antes e depois dos saques nativos.
   * `scripts_e_dados/Metricas/resumo_metricas.json` — Resumo estatístico para consumo em programas ou scripts.

3. **Gráficos para Inserir na Monografia (300 DPI):**
   * `scripts_e_dados/Graficos/fig01_depeg_historico_steth.png`
   * `scripts_e_dados/Graficos/fig02_depeg_pre_pos_shanghai.png`
   * `scripts_e_dados/Graficos/fig03_histograma_distribuicao_depeg.png`
   * `scripts_e_dados/Graficos/fig04_rendimento_apr_lido_vs_solo.png`
   * `scripts_e_dados/Graficos/fig05_evolucao_tvl_lido_vs_preco_eth.png`
   * `scripts_e_dados/Graficos/fig06_market_share_historico_lsd.png`
   * `scripts_e_dados/Graficos/fig07_dispersao_market_share_vs_depeg.png`
   * `scripts_e_dados/Graficos/fig08_indice_hhi_concentracao.png`

---

## 💡 Solução de Problemas (Troubleshooting)

* **Erro de Rate Limit na API (429):** As APIs públicas da DefiLlama não exigem API key. Caso receba aviso de *rate limit*, aguarde alguns instantes; os scripts já possuem rotinas automáticas de pausa (`time.sleep`).
* **Caracteres no Terminal Windows:** Se o seu PowerShell exibir caracteres estranhos em mensagens do terminal, execute antes `$OutputEncoding = [System.Text.Encoding]::UTF8`.
