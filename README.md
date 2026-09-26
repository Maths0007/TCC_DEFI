# TCC — Finanças Descentralizadas (DeFi): Análise Empírica do Protocolo Lido DAO e da Dinâmica do Staking Líquido (stETH) no Ecossistema Ethereum

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maths0007/TCC_DEFI/blob/master/notebook_tcc_lido_defi.ipynb)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Data Integrity](https://img.shields.io/badge/data%20integrity-SHA--256%20verified-green.svg)](fontes/manifesto.json)
[![Zero Imputation](https://img.shields.io/badge/methodology-100%25%20real%20data%20%7C%20no%20synthetic%20fill-orange.svg)](scripts_e_dados/DADOS_DO_TCC/DICIONARIO_DE_DADOS.md)

Repositório oficial de dados, códigos, pipeline analítica auditada, gráficos acadêmicos e apresentação do **Trabalho de Conclusão de Curso (TCC)** desenvolvido no âmbito da **Universidade Federal de Campina Grande (UFCG)**.

---

## 📌 1. Visão Geral do Projeto

A transição da rede Ethereum do mecanismo de consenso *Proof-of-Work* (PoW) para *Proof-of-Stake* (PoS) — consolidada pelo evento do **The Merge** em setembro de 2022 — inaugurou uma nova dinâmica econômica ancorada na validação via bloqueio de capital (*staking*). O protocolo **Lido DAO** emergiu como a principal solução de **Liquid Staking Derivatives (LSD / LST)**, emitindo o token sintético **stETH** como representação fungível e negociável do ETH bloqueado na *Beacon Chain*.

### Objetivos Centrais da Pesquisa:
1. **Dinâmica de Descolamento (*Depeg*) do stETH**: Investigar os determinantes do desvio entre o preço de mercado do stETH e do ETH nativo, com foco na paridade teórica 1:1 e no prêmio/desconto de liquidez.
2. **Impacto Estrutural do *Hard Fork Shanghai/Capella* (Abril de 2023)**: Mensurar econometricamente como a habilitação técnica dos saques (*withdrawals*) on-chain alterou a eficiência de precificação e a volatilidade do desconto do stETH.
3. **Economia do Staking e APR**: Analisar o comportamento temporal da taxa de rendimento da rede (*ETH.STORE*) frente à expansão expressiva do volume de ETH em validação (diluição de recompensas).
4. **Resiliência em Momentos de Estresse de Liquidez**: Avaliar o comportamento do par stETH/ETH durante eventos sistêmicos do mercado cripto (colapsos da Terra/LUNA, Celsius Network e exchange FTX em 2022).

---

## 📂 2. Arquitetura e Organização do Repositório

Todos os scripts em Python foram centralizados de forma modular e canônica na pasta [`scripts_e_dados/scripts/`](file:///d:/TCC_DEFI/scripts_e_dados/scripts), mantendo a raiz do repositório limpa e acessível:

```text
TCC_DEFI/
├── README.md                           # Documentação técnica e guia metodológico completo
├── requirements.txt                   # Dependências do projeto (pandas, numpy, scipy, yfinance, etc.)
├── notebook_tcc_lido_defi.ipynb       # Jupyter Notebook autossuficiente para Google Colab
├── .gitignore                         # Regras de exclusão de binários e arquivos temporários
│
├── fontes/                            # 🏛️ FONTES PRIMÁRIAS E MANIFESTO CRIPTOGRÁFICO
│   ├── manifesto.json                 # Hashes SHA-256 e proveniência de todos os dados brutos
│   ├── apr/                           # Dados brutos de rendimento da rede (ETH.STORE)
│   └── staking/                       # Dados brutos de validação da Beacon Chain
│
├── artigos/                           # 📚 BASE BIBLIOGRÁFICA E ARTIGOS CITADOS NO TCC
│   ├── INDICE_DE_ARTIGOS.md           # Catálogo com tabela ABNT de todas as 13 obras citadas
│   ├── artigos_usados_no_tcc/         # PDFs dos artigos e whitepapers utilizados no texto
│
├── scripts_e_dados/
│   ├── scripts/                       # ⚙️ TODOS OS SCRIPTS EM PYTHON DO PROJETO
│   │   ├── comum_tcc.py               # Constantes, calendário UTC (Maio/22 a Maio/26) e utilitários
│   │   ├── 01_coleta_precos.py        # Coleta Yahoo Finance (ETH-USD e STETH-USD) e volatilidades
│   │   ├── 02_coleta_rated_network.py # Consolidação de validadores on-chain
│   │   ├── 02a_coleta_staking_rewards.py # Extração e auditoria da Beaconcha.in (ETH.STORE)
│   │   ├── 03_coleta_defillama_curve.py  # Coleta DeFiLlama (liquidez e pools Curve)
│   │   ├── 04_consolidar_dataset.py   # Fusão temporal e cálculo estrito de métricas
│   │   ├── formatar_dataset.py        # Padronização e ordenação das colunas de saída
│   │   ├── validar_dados_tcc.py       # Auditor formal de integridade e completude
│   │   ├── 05_gerar_graficos_tcc.py   # Geração dos gráficos acadêmicos em alta resolução (300 DPI)
│   │   ├── organizar_dados_intuitivos.py # Gerador dos datasets temáticos e relatórios limpos
│   │   ├── executar_pipeline.py       # Orquestrador oficial com parâmetros configuráveis
│   │   ├── coletar_todos.py           # Wrapper de execução rápida com um único comando
│   │   └── testar_pipeline.py         # Bateria de 8 testes unitários automatizados
│   │
│   ├── DADOS_DO_TCC/                  # 📊 DATASETS FINAIS ORGANIZADOS E INTUITIVOS
│   │   ├── dataset_consolidado_tcc.csv # Base principal (11 variáveis essenciais, 1.492 observações)
│   │   ├── dados_precos_e_depeg.csv    # Série de preços, razão stETH/ETH, depeg e retornos
│   │   ├── dados_staking_e_apr.csv     # Série de saldo em staking e rendimento ETH.STORE
│   │   ├── DICIONARIO_DE_DADOS.md     # Dicionário detalhado com fórmulas, unidades e fontes
│   │   └── tecnico_auditoria/         # Dados brutos completos com 36 colunas e metadados
│   │       ├── dataset_completo_com_metadados.csv
│   │       ├── auditoria_tcc.json
│   │       └── execucao.json
│   │
│   ├── Graficos/                      # 📈 FIGURAS ACADÊMICAS EM ALTA RESOLUÇÃO (300 DPI)
│   │   ├── mercado_steth.png          # Painel temporal de preços e descolamento (depeg %)
│   │   └── staking_apr_rede.png       # Painel de saldo em staking vs. taxa APR anual
│   │
│   └── Metricas/                      # 📑 RELATÓRIOS ESTATÍSTICOS E ECONOMÉTRICOS
│       ├── relatorio_metricas_atualizado.md # Relatório formatado (Pré vs. Pós-Shanghai)
│       └── resumo_metricas_atualizado.json  # Síntese estruturada em JSON
│
└── apresentacao/                      # 🎓 SLIDES E APRESENTAÇÃO DO TCC
    ├── index.html                     # Apresentação interativa em HTML/CSS/JS
    ├── script.js                      # Interatividade da apresentação
    ├── style.css                      # Identidade visual acadêmica (UFCG Navy & Teal)
    └── gerar_pptx.py                  # Script gerador da apresentação em PowerPoint (.pptx)
```

---

## ⚙️ 3. Catálogo Detalhado dos Scripts (`scripts_e_dados/scripts/`)

A pipeline foi desenhada seguindo o princípio da **reprodutibilidade determinística**:

| Script | Função Principal | Entradas / Fontes | Saídas / Produtos |
| :--- | :--- | :--- | :--- |
| [`comum_tcc.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/comum_tcc.py) | Módulo central de suporte. Define o grid temporal UTC (`2022-05-01` a `2026-05-31`), caminhos canônicos e validações matemáticas. | Variáveis de ambiente (`TCC_*`) | Utilitários de hash, grid temporal e assertivas |
| [`01_coleta_precos.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/01_coleta_precos.py) | Coleta cotações diárias de mercado de `ETH-USD` e `STETH-USD` via Yahoo Finance. Calcula retornos logarítmicos e volatilidades móveis de 30 dias anualizadas. **Zero preenchimento artificial.** | Yahoo Finance API (`yfinance`) | `precos_mercado.csv` |
| [`02a_coleta_staking_rewards.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/02a_coleta_staking_rewards.py) | Extrai dados da Beacon Chain e ETH.STORE. Audita rigorosamente a fórmula percentual do APR: $\text{APR} = \frac{\text{recompensas}}{\text{saldo\_efetivo}} \times 365 \times 100$. | `fontes/apr/`, `fontes/staking/` | `ethstore_extraido.csv`, `auditoria_ethstore.json` |
| [`02_coleta_rated_network.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/02_coleta_rated_network.py) | Consolida métricas on-chain de validadores ativos, operadores e taxas da rede. | Fontes locais / API Rated | `rated_consolidado.csv` |
| [`03_coleta_defillama_curve.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/03_coleta_defillama_curve.py) | Extrai séries históricas de TVL e liquidez da pool stETH/ETH da Curve Finance. | DeFiLlama Yields API | `defillama_curve.csv` |
| [`04_consolidar_dataset.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/04_consolidar_dataset.py) | Realiza o *merge* estrito baseado no calendário civil UTC. Calcula o descolamento ($\text{depeg\_pct} = (\frac{\text{stETH}}{\text{ETH}} - 1) \times 100$) e alinha metadados. | Séries processadas das etapas 01 a 03 | `dataset_consolidado_tcc.csv` bruto |
| [`formatar_dataset.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/formatar_dataset.py) | Reorganiza as colunas de forma padronizada, posicionando as variáveis de preços e depeg nas primeiras posições. | Dataset bruto | `dataset_final_tcc.csv` |
| [`validar_dados_tcc.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/validar_dados_tcc.py) | Validador de integridade formal. Rejeita dados faltantes no escopo contratado, duplicatas e inconsistências lógicas. | Dataset final | `auditoria_tcc.json` |
| [`05_gerar_graficos_tcc.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/05_gerar_graficos_tcc.py) | Plota gráficos científicos com formatação para monografia (estilo acadêmico, 300 DPI, anotações de marcos históricos). | `dataset_final_tcc.csv` | `mercado_steth.png`, `staking_apr_rede.png` |
| [`organizar_dados_intuitivos.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/organizar_dados_intuitivos.py) | Cria a pasta amigável `DADOS_DO_TCC/` com as 11 colunas econômicas limpas, gera o dicionário em Markdown e computa as estatísticas descritivas Pré vs. Pós-Shanghai. | `dataset_final_tcc.csv` | `DADOS_DO_TCC/`, `Metricas/` |
| [`executar_pipeline.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/executar_pipeline.py) | Orquestrador principal da pipeline com tratamento de exceções, flags de modo (`--offline`, `--somente-beaconchain`) e registro de execução. | Argumentos CLI | `execucao.json` |
| [`coletar_todos.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/coletar_todos.py) | Ponto de entrada simplificado para execução rápida com parâmetros verificados por padrão. | Linha de comando | Execução completa da pipeline |
| [`testar_pipeline.py`](file:///d:/TCC_DEFI/scripts_e_dados/scripts/testar_pipeline.py) | Suíte de testes unitários que valida hashes de entrada, ausência de duplicatas, tratamento de lacunas e consistência da auditoria sem requisições de rede. | Módulos locais | Relatório `OK` de 8 testes |

---

## 📊 4. Datasets Prontos para Análise (`DADOS_DO_TCC/`)

Para facilitar o trabalho econométrico, criamos uma camada de dados limpa em [`scripts_e_dados/DADOS_DO_TCC/`](file:///d:/TCC_DEFI/scripts_e_dados/DADOS_DO_TCC):

### 📄 `dataset_consolidado_tcc.csv` (1.492 linhas, 11 colunas)

| Coluna | Unidade | Descrição Conceitual |
| :--- | :--- | :--- |
| `data` | AAAA-MM-DD | Data civil de referência em UTC (01/05/2022 a 31/05/2026). |
| `total_eth_staked` | ETH | Volume total de ETH efetivamente em validação na Beacon Chain. |
| `apr_rede_ethstore_pct` | % a.a. | Taxa anualizada de rendimento da rede Ethereum (ETH.STORE) em janelas de 24h. |
| `preco_eth_usd` | USD ($) | Preço de fechamento diário do Ether nativo (Yahoo Finance: `ETH-USD`). |
| `preco_steth_usd` | USD ($) | Preço de fechamento diário do Lido Staked ETH (Yahoo Finance: `STETH-USD`). |
| `razao_steth_eth` | Ratio | Razão direta de paridade de preços: $\frac{P_{stETH}}{P_{ETH}}$ (paridade teórica = 1,000000). |
| `depeg_pct` | % | Desvio percentual relativo à paridade: $\left(\frac{P_{stETH}}{P_{ETH}} - 1\right) \times 100$. |
| `retorno_log_eth` | Decimal | Retorno logarítmico diário do ETH: $\ln(P_t / P_{t-1})$. |
| `retorno_log_steth` | Decimal | Retorno logarítmico diário do stETH: $\ln(P_t / P_{t-1})$. |
| `volatilidade_anual_eth_30d` | % a.a. | Volatilidade móvel anualizada de 30 dias do ETH ($\sigma_{30d} \times \sqrt{365} \times 100$). |
| `volatilidade_anual_steth_30d` | % a.a. | Volatilidade móvel anualizada de 30 dias do stETH. |

> Consulte [`DADOS_DO_TCC/DICIONARIO_DE_DADOS.md`](file:///d:/TCC_DEFI/scripts_e_dados/DADOS_DO_TCC/DICIONARIO_DE_DADOS.md) para obter o dicionário estendido, limites analíticos e considerações metodológicas.

---

## 🔬 5. Rigor Metodológico e Princípios Científicos

1. **Zero Imputação Artificial**: A literatura econométrica adverte que preenchimentos arbitrários (como *linear interpolation* ou *forward-fill* descontrolado) distorcem artificialmente a variância e geram autocorrelação espúria em testes de raiz unitária e cointegração. Todas as séries respeitam estritamente as observações empíricas reais de mercado.
2. **Autenticação Criptográfica por Hash SHA-256**: Cada fonte primária armazenada em `fontes/` possui seu digest SHA-256 computado e registrado no [`fontes/manifesto.json`](file:///d:/TCC_DEFI/fontes/manifesto.json). A pipeline testa a conformidade dos dados brutos a cada execução.
3. **Harmonização Temporal UTC Estrita**: O período de 24 horas do ETH.STORE (iniciado às 12:00:23 UTC) é indexado à sua respectiva data civil de abertura, alinhado aos fechamentos de mercado em UTC.
4. **Respeito ao Recorte do TCC**: Amostra padronizada de **1.492 observações diárias** consecutivas, cobrindo de **01 de maio de 2022** a **31 de maio de 2026**.

---

## 📈 6. Principais Resultados Empíricos

Os dados consolidados pela pipeline revelam evidências econométricas consistentes:

### A. Estatísticas Descritivas do Descolamento (*Depeg*)

- **Total de Observações**: 1.492 dias
- **Depeg Médio Global**: **-0,5127%**
- **Depeg Mediano Global**: **-0,1267%**
- **Desvio Padrão Global**: **0,9739%**
- **Pico de Maior Desconto (Mínimo Histórico)**: **-6,3263%** (Crise de liquidez após o colapso da Terra/LUNA e insolvência da Celsius Network em junho de 2022)
- **Maior Prêmio (Máximo Histórico)**: **+1,0851%**

### B. Impacto do Hard Fork Shanghai/Capella (12 de Abril de 2023)

A ativação dos saques on-chain (*withdrawals*) transformou estruturalmente a natureza do stETH:

| Período | Dias | Depeg Médio (%) | Desvio Padrão (%) | Interpretação |
| :--- | :---: | :---: | :---: | :--- |
| **Pré-Shanghai** (Sem saques: Maio/2022 a Abr/2023) | 347 | **-1,8218%** | **1,3085%** | Alto desconto de iliquidez e volatilidade expressiva |
| **Pós-Shanghai** (Com saques: Abr/2023 a Mai/2026) | 1.145 | **-0,1159%** | **0,2019%** | Arbitragem eficiente e forte ancoragem à paridade |

> 💡 **Conclusão Econométrica:** A habilitação dos saques reduziu a volatilidade do descolamento em **84,6%**, eliminando quase totalmente o desconto estrutural de iliquidez do stETH.

### C. Crescimento do Staking vs. Rendimento da Rede

- **Expansão do Saldo em Staking**: O total de ETH bloqueado na rede saltou de **11.625.590 ETH** em maio de 2022 para **39.255.940 ETH** em maio de 2026 — um crescimento de **+237,7%**.
- **Taxa APR Média da Rede**: **3,751% a.a.** (mínimo de 2,536% a.a. e máximo de 8,618% a.a.), exibindo a tendência esperada de diluição de rendimento conforme o protocolo absorve mais validadores.

---

## 🚀 7. Como Reproduzir a Pesquisa

### Pré-requisitos
- Python 3.10 ou superior.
- Git (opcional, para versionamento).

### Passo 1: Clonar o Repositório e Criar Ambiente Virtual
```bash
git clone https://github.com/Maths0007/TCC_DEFI.git
cd TCC_DEFI

# Criar ambiente virtual
python -m venv .venv

# Ativar no Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Ou ativar no Linux/macOS:
source .venv/bin/activate
```

### Passo 2: Instalar as Dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Executar a Bateria de Testes Unitários
```bash
python scripts_e_dados/scripts/testar_pipeline.py
```
*(Deverá exibir 8 testes executados com status `OK`)*.

### Passo 4: Executar a Pipeline

**Modo Verificado (Fontes Oficiais Beaconcha.in / ETH.STORE):**
```bash
python scripts_e_dados/scripts/executar_pipeline.py --somente-beaconchain --offline
```

**Atualizar Coleta de Preços de Mercado (Yahoo Finance):**
```bash
python scripts_e_dados/scripts/01_coleta_precos.py
```

**Gerar Datasets Intuitivos e Recalcular Métricas:**
```bash
python scripts_e_dados/scripts/organizar_dados_intuitivos.py
```

### Passo 5: Execução via Google Colab
Caso prefira não executar localmente, utilize o notebook interativo no Google Colab clicando no botão abaixo:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maths0007/TCC_DEFI/blob/master/notebook_tcc_lido_defi.ipynb)

---

## 🎓 8. Apresentação e Recursos de Defesa

O repositório inclui os recursos de apoio para a banca examinadora na pasta [`apresentacao/`](file:///d:/TCC_DEFI/apresentacao):
- [`index.html`](file:///d:/TCC_DEFI/apresentacao/index.html): Apresentação interativa de slides em formato web responsivo (pode ser aberta em qualquer navegador).
- [`gerar_pptx.py`](file:///d:/TCC_DEFI/apresentacao/gerar_pptx.py): Script automatizado com `python-pptx` para gerar a apresentação oficial em PowerPoint (`Apresentacao_TCC_Matheus.pptx`, 11 slides widescreen 16:9 na paleta UFCG Navy & Teal).

---

## 📚 9. Referências Bibliográficas e Artigos do TCC

Todas as 13 fontes primárias, artigos científicos e whitepapers citados no texto da monografia estão disponíveis na pasta [`artigos/artigos_usados_no_tcc/`](file:///d:/TCC_DEFI/artigos/artigos_usados_no_tcc), acompanhados de seus respectivos resumos analíticos em [`artigos/fichamentos/`](file:///d:/TCC_DEFI/artigos/fichamentos).

> 📖 **Consulte o catálogo completo:** [`artigos/INDICE_DE_ARTIGOS.md`](file:///d:/TCC_DEFI/artigos/INDICE_DE_ARTIGOS.md)

Principais referências citadas no texto:
- **BUTERIN, V.** *Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform*. Whitepaper, 2014.
- **CARRÉ, S.; GABRIEL, F.** *Liquid Staking: When Does It Help?* SSRN Electronic Journal, 2025.
- **CINTRA, T. N.; HOLLOWAY, M. P.** *Detecting Depegs: Towards Safer Passive Liquidity Provision on Curve Finance*. arXiv:2306.10612, 2023.
- **CONG, L. W.; HE, Z.; TANG, K.** *The Tokenomics of Staking*. NBER Working Paper 33640, 2025.
- **HARVEY, C. R.; RAMACHANDRAN, A.; SANTORO, J.** *DeFi and the Future of Finance*. Hoboken: John Wiley & Sons, 2021.
- **JIN, M.; LIU, R.; MONPERRUS, M.** *On-Chain Analysis of Smart Contract Dependency Risks on Ethereum*. arXiv:2503.19548, 2025.
- **LIDO DAO.** *Lido: Ethereum Liquid Staking*. Whitepaper, 2020. Disponível em: <https://lido.fi/>.
- **LIM, K. Y.** *KelpDAO Exploit Analysis and Restaking Protocol Risks*. Binance Research, 2026.
- **MAKAROV, I.; SCHOAR, A.** *Cryptocurrencies and Decentralized Finance (DeFi)*. Brookings / NBER, 2022.
- **NABBEN, K.; DE FILIPPI, P.** *Governance of Decentralized Autonomous Organizations*. SSRN, 2024.
- **SCHARNOWSKI, S.; JAHANSHAHLOO, H.** *The Economics of Liquid Staking Derivatives: Basis Determinants and Price Discovery*. Journal of Futures Markets, v. 45, n. 1, p. 91–117, 2025.
- **SCHÄR, F.** *Decentralized Finance: On Blockchain- and Smart Contract-Based Financial Markets*. Federal Reserve Bank of St. Louis Review, v. 103, n. 2, p. 153–174, 2021.
- **XIONG, X. et al.** *Leverage Staking with Liquid Staking Derivatives (LSDs): Opportunities and Risks*. arXiv:2401.08610, 2024.

---

## 📄 10. Licença e Direitos Autorais

Este projeto foi desenvolvido para fins estritamente acadêmicos e científicos no âmbito da Universidade Federal de Campina Grande (UFCG).  
