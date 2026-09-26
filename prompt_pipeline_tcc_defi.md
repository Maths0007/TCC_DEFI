# Prompt de Engenharia de Dados DeFi & Pipeline Quantitativo 

> **Instruções de Uso:** Copie o bloco de texto abaixo e envie ao modelo de linguagem/assistente para gerar integralmente o pipeline modular de engenharia de dados, auditoria quantitativa e visualização acadêmica.

```markdown
Atue como um Engenheiro de Dados Quantitativos e Desenvolvedor Python especializado em Finanças Descentralizadas (DeFi) e Mercados de Capitais Digitais.

Desenvolva um pipeline de dados modular, reprodutível e robusto em Python para coleta, tratamento, consolidação, auditoria quantitativa e renderização de gráficos acadêmicos em alta resolução (300 DPI) para uma pesquisa acadêmica/TCC com o seguinte tema e especificações metodológicas:

---

### 1. CONTEXTO, ESCOPO E PARÂMETROS GERAIS

- **Tema da Pesquisa:** Finanças Descentralizadas: A avaliação do liquid staking via Lido DAO como alternativa de investimento em ativos digitais.
- **Recorte Temporal Estrito:** `2022-05-05` a `2026-05-31` (frequência diária contínua em UTC, exatamente 1.488 observações sem lacunas ou finais de semana vazios).
- **Stack Tecnológica:** Python 3.10+, `pandas`, `numpy`, `requests`, `yfinance`, `concurrent.futures`, `matplotlib`, `seaborn`, `python-dotenv`.
- **Estrutura de Diretórios:**
  - `Dados/` (para arquivos `.csv` intermediários e o dataset master)
  - `Graficos/` (para as figuras acadêmicas em 300 DPI)
  - Raiz do projeto com scripts executáveis independentemente e por orquestrador mestre.

---

### 2. ARQUITETURA MODULAR REQUERIDA

Gere o código Python completo, funcional e documentado para cada um dos seguintes módulos:

#### Módulo 1: Coleta de Preços de Mercado, Volatilidade e Depeg (`01_coleta_precos.py`)
- **Fontes:** `yfinance` (`ETH-USD` e `STETH-USD`) com sistema de contingência automática via DefiLlama Coins API (`https://coins.llama.fi/prices/historical/{ts}/{coin_id}`) para datas faltantes.
- **Grid Contínuo:** Alinhar em um grid diário UTC de `2022-05-05` a `2026-05-31`, preenchendo lacunas residuais com interpolação linear suave.
- **Métricas Calculadas:**
  1. Taxa de Câmbio Direta (Preço Relativo no Mercado Secundário):
     $$\text{preco\_steth\_eth} = \frac{\text{preco\_steth\_usd}}{\text{preco\_eth\_usd}}$$
  2. Liquid Staking Basis:
     $$\text{basis} = \text{preco\_steth\_eth} - 1.0000$$
  3. Descolamento Percentual (Depeg %):
     $$\text{depeg\_pct} = \text{basis} \times 100$$
  4. Retornos Logarítmicos Diários de ETH e stETH:
     $$r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)$$
  5. Volatilidade Realizada de 7 dias e 30 dias anualizada:
     $$\sigma_{\text{anual}} = \sigma_{\text{janela}} \times \sqrt{365} \times 100$$
- **Saída:** `Dados/dados_precos_mercado.csv`.

---

#### Módulo 2: Camada de Consenso e Staking Direto (`02_coleta_rated_network.py`)
- **Metodologia Teórico-Empírica:**
  1. Construir a série temporal de Total de ETH em Stake na Beacon Chain ($S_t$) a partir dos marcos oficiais da rede (Merge, Shapella, etc.) com interpolação linear diária.
  2. Aplicar a fórmula de emissão oficial da Beacon Chain:
     $$\text{APR}_{\text{consenso}} (\%) = \frac{16.632,32}{\sqrt{S_t}}$$
  3. Coletar série histórica real de APY do Lido stETH via DefiLlama Yields API (`Pool UUID: 747c1d2a-c668-4682-b9f9-296708a3dd90`) e converter APY efetivo para APR nominal diário ($n=365$).
  4. Mesclar com a taxa de MEV dos relays para obter:
     $$\text{APR}_{\text{rede\_direto\_total\_pct}} = \text{APR}_{\text{consenso\_bruto\_pct}} + \text{taxa\_mev\_execucao\_apr\_pct}$$
- **Saída:** `Dados/dados_rated_consenso.csv`.

---

#### Módulo 2b: Coleta Concorrente de MEV via Relays MEV-Boost (`02b_coleta_mev_relay.py`)
- **Fontes:** Data API pública dos relays MEV-Boost (Flashbots, Ultra Sound, Aestus, Agnostic).
- **Processamento Concorrente:** Executar via `concurrent.futures.ThreadPoolExecutor(max_workers=20)` com timeout de 2.5s por requisição.
- **Regras de Negócio:**
  - Converter datas para slots da Beacon Chain (12s por slot desde o Genesis UTC `1606824023`).
  - MEV zerado para datas anteriores ao *The Merge* (`2022-09-15`).
  - Calcular valor total diário de MEV (valor médio por bloco $\times$ 7.200 slots/dia).
  - Calcular taxa de rendimento de execução anualizada ($\%\text{ a.a.}$):
    $$\text{taxa\_mev\_execucao\_apr\_pct} = \frac{\text{mev\_total\_diario\_eth} \times 365}{S_t} \times 100$$
- **Saída:** `Dados/dados_mev_relay.csv`.

---

#### Módulo 3: TVL Global do Ethereum, Lido e Pool Curve (`03_coleta_defillama_curve.py`)
- **Fontes:**
  - DefiLlama Charts: TVL total do ecossistema Ethereum (`https://api.llama.fi/charts/Ethereum`).
  - DefiLlama Protocol: TVL total e TVL Ethereum da Lido DAO (`https://api.llama.fi/protocol/lido`).
  - DefiLlama Yields: Histórico de TVL e APY da Pool Curve stETH/ETH (`Pool UUID: 57d30b9c-fc66-4ac2-b666-69ad5f410cce`).
- **Métricas:**
  - Participação de mercado / Dominância da Lido:
    $$\text{dominancia\_lido\_tvl\_defi\_pct} = \left(\frac{\text{tvl\_lido\_ethereum\_usd}}{\text{tvl\_rede\_ethereum\_total\_usd}}\right) \times 100$$
- **Saída:** `Dados/dados_defillama_curve.csv`.

---

#### Módulo 4: Consolidação do Master Dataset (`04_consolidar_dataset.py`)
- **Merge & Alinhamento:** Unificar todas as tabelas no grid de 1.488 linhas diárias UTC.
- **Categorização & Eventos:**
  - Variável categórica de regime: `Pre-Merge` ($< 2022\text{-}09\text{-}15$), `Post-Merge_Pre-Shapella` ($< 2023\text{-}04\text{-}12$), `Post-Shapella` ($\ge 2023\text{-}04\text{-}12$).
  - Dummies binárias ($0$ ou $1$) para janelas de choque: Crash Terra/Luna, The Merge, Crash FTX e Hard Fork Shapella.
- **Métricas Financeiras de Spread:**
  1. Spread Real Independente (Delta APR):
     $$\Delta\text{APR}_t = \text{APR}_{\text{rede\_direto\_total\_pct}} - \text{APR}_{\text{lido\_liquido\_pct}}$$
  2. Taxa de Retenção Efetiva da Lido DAO (\%):
     $$\text{taxa\_retencao\_efetiva\_pct} = \left(\frac{\Delta\text{APR}_t}{\text{APR}_{\text{rede\_direto\_total\_pct}}}\right) \times 100$$
  3. Custo de Oportunidade Diário e Acumulado.
- **Formatação:** Tipagem estrita, arredondamentos decimais adequados para cada grandeza (moeda, taxas e retornos).
- **Saída:** `Dados/dataset_master_tcc_2022_2026.csv`.

---

#### Módulo 5: Renderização de Figuras Acadêmicas 300 DPI (`05_gerar_graficos_tcc.py`)
- **Padrão Gráfico:** Estilo limpo (`seaborn-v0_8-whitegrid`), tipografia legível, sem caixas de legenda opacas ou poluição visual, exportação em 300 DPI via `matplotlib.pyplot.savefig(bbox_inches="tight")`.
- **Gráficos:**
  1. `grafico_01_paridade_depeg_2022_2026.png`:
     - Subplot 1 (topo): Série temporal da taxa de câmbio stETH/ETH vs paridade teórica (1.0000) com área sombreada de desconto.
     - Subplot 2 (base): Depeg % (Basis) com linhas de referência para limites críticos (-2.0% e -5.0%).
     - Linhas verticais e caixas de anotação com setas nos eventos históricos (Terra/Luna, The Merge, Shapella).
  2. `grafico_02_comparativo_apr_retornos.png`:
     - Subplot 1 (topo): Curva do APR Staking Direto vs APR Líquido do stETH com área sombreada destacando a comissão retida pelo protocolo.
     - Subplot 2 (base): Série diária do $\Delta\text{APR}_t$ com linha tracejada da média histórica.

---

#### Módulo 6: Auditoria Quantitativa e Orquestrador Mestre (`validar_dados_tcc.py` e `executar_pipeline.py`)
- **Validador Quantitativo (`validar_dados_tcc.py`):**
  - Implementar suíte de asserções cobrindo:
    1. Dimensões exatas (1.488 linhas sem gaps ou duplicatas).
    2. Positividade estrita de preços e TVL.
    3. Consistência matemática das identidades ($\Delta\text{APR}$, Depeg, Paridade, Consenso + MEV).
    4. Faixa empírica da taxa de retenção da Lido DAO ($8.7\%$ a $10.5\%$).
    5. Captura do estresse severo de liquidez no Crash Luna/Terra (depeg $\le -5.0\%$).
    6. Estabilização e convergência da paridade pós-Shapella ($|\text{depeg}| < 0.5\%$).
    7. Variabilidade de todas as variáveis contínuas (std > 0, sem achatamento sintético).
- **Orquestrador Mestre (`executar_pipeline.py`):**
  - Execução sequencial dos scripts via `subprocess.run`, medição de tempo de execução e log de resumo ao final.

---

### 3. DIRETRIZES DE QUALIDADE DO CÓDIGO
- Inclua docstrings explicativas e type hints em todas as funções.
- Trate exceções de rede HTTP (`try/except`, status codes, fallbacks e timeouts).
- Exiba relatórios informativos de estatísticas descritivas (médias, mínimos, máximos e contagens) no terminal ao término da execução de cada módulo.
```
### Foi usado o Claude Sonnet 5 via Claude terminal e o Gemini 3.7 flash high via Antigravity Ide para refinar o código
