# Fichamento Analítico: Empirical and Theoretical Analysis of Liquid Staking Protocols

**Referência Bibliográfica:**
GOGOL, K.; KRANER, B.; SCHLOSSER, M.; YAN, T.; TESSONE, C.; STILLER, B. *Empirical and Theoretical Analysis of Liquid Staking Protocols*. arXiv preprint arXiv:2401.16353v1, 2024.

---

## 1. Problema de Pesquisa e Motivação
A pesquisa foca em compreender as implementações, fundamentos operacionais e riscos de depeg envolvendo protocolos de Liquid Staking (LSPs) nos maiores blockchains baseados em Proof-of-Stake (Ethereum, Solana e BNB Chain). Os autores testam se os Liquid Staking Tokens (LSTs), sendo ativos derivativos sintéticos (*pegged assets*), de fato refletem e entregam com precisão os retornos oriundos do staking direto, e investigam como choques de mercado e imperfeições (autocorrelação e assimetria de informações) desalinham o Valor de Mercado (*Market Value*) do Valor Justo (*Fair/Peg Value*).

---

## 2. Abordagem Teórica (Fundamentação e Taxonomia)
Para estruturar seu embasamento, o artigo elabora uma robusta taxonomia para LSPs, muito importante para categorizar tecnicamente a Lido e as competidoras no TCC.

### Modelos de Distribuição de Recompensa (Token Models):
- **Rebase Token (ex: Lido stETH):** O protocolo inflaciona o suprimento para refletir os rendimentos. O token mantém a paridade nominal 1:1 ao ETH base. A desvantagem é a falta de composabilidade direta em alguns DEXs, muitas vezes exigindo um *wrapper* (wstETH).
- **Reward-bearing Token (ex: Lido wstETH, RocketPool rETH, Coinbase cbETH):** O token captura os rendimentos valorizando-se com o passar do tempo e não preserva a paridade 1:1 estritamente. Tem plena composabilidade no ecossistema DeFi.
- **Dual Token (ex: StakeWise):** O capital apostado e as recompensas são desdobrados em tokens diferentes (sETH2 para o principal e rETH2 para as recompensas), fragmentando a liquidez.

### Conceito Crítico de Precificação:
- **Fair/Peg Value (Valor Justo):** É determinado pelo saldo da reserva de tokens subjacentes guardados no protocolo e geradores de *yield*. Se houver garantia de conversão imediata e sem atritos, ditaria o preço de negociação.
- **Market Value (Valor de Mercado):** É a cotação pela qual o LST é liquidado e flutua nos mercados secundários (DEXs/CEXs) baseada em oferta, demanda e incertezas institucionais.

---

## 3. Metodologia (Abordagem Quantitativa)
- **Base de Dados:** Os pesquisadores rastrearam os preços secundários históricos (fontes: UniSwap e Yahoo Finance) dos maiores LSTs e os compararam aos retornos de *staking* diretos das suas respectivas blockchains nativas.
- **Análise Econométrica:** Executaram múltiplas Regressões OLS (Método dos Mínimos Quadrados) multivariadas, isolando os "Excedentes de Retorno" (*Excess Returns*) frente ao *staking* bruto, e controlaram variáveis macro como Volatilidade diária, Retorno de preço do ativo-mãe, Capitalização de Mercado e Volume Tracionado.
- **Autocorrelação:** Implementaram modelos Auto-regressivos AR(p) para determinar as latências dos prêmios ou descontos da relação *peg*.

---

## 4. Resultados Analíticos e Empíricos Detalhados

### Rendimento e Erro de Rastreamento (*Tracking Error*)
- O prêmio entregue pelos LSTs se correlaciona intimamente com as taxas de recompensas oferecidas pela blockchain correspondente. Todavia, os LSTs registraram retornos residuais ligeiramente negativos. Isso ocorre devido às **taxas comissionadas cobradas pela governança** (ex. 10% cobrado pelo Lido DAO) e por pequenas flutuações de spread.

### Impactos de Eventos de Estresse (Terra e FTX)
- A pesquisa constatou uma disrupção mensurável no rastreamento de valor originada pelo medo de contágio (*market inefficiencies*).
- **Colapso da Terra/LUNA (Maio de 2022):** Causou forte liquidação. O Token da Lido (stETH) e RocketPool (rETH) sofreram descontos expressivos operando abaixo do valor justo (*undervalued*), pois o pânico no mercado suplantou a capacidade instantânea dos arbitradores de equacionar as paridades, gerando risco severo aos investidores alavancados.
- **Insolvência da FTX (Novembro de 2022):** Resultou em uma anomalia contrária: Tokens como o rETH começaram a ser negociados supervalorizados (*overvalued*) em relação ao seu peg. Por que isso ocorreu? O rETH é emitido por um protocolo permissivo (RocketPool), considerado mais **descentralizado**. A quebra da corretora FTX instilou nos usuários a fobia pelo risco centralizado, promovendo um prêmio de liquidez pela "confiança em contratos estritamente não-custodiais".

### Modelagem Autoregressiva (O Problema do Depeg Persistente)
A regressão concluiu algo revelador:
- A disparidade (Desconto/Prêmio) entre o valor de mercado e o valor justo do LST **não** se relaciona intimamente a parâmetros macroeconômicos tradicionais da criptomoeda base (como volume financeiro ou flutuação de preço).
- Ao invés disso, ela obedece rigorosamente a fatores **autoregressivos**. O desconto num dia "t" explica positivamente o desconto no dia "t+1". Isso demonstra que o mercado sofre de assimetria de liquidez persistente: uma vez instaurado um *depeg*, ele possui uma inércia temporal de até 6 dias na modelagem, provando que o protocolo Lido pode demorar para reabsorver desequilíbrios na Curve.

---

## 5. Implicações Estratégicas para o TCC
*Este estudo consolida os pilares quantitativos que devemos usar na escrita da monografia.*
1. **Taxonomia para a Introdução/Fundamentação:** Fornece a melhor arquitetura conceitual para os primeiros subcapítulos do seu trabalho: defina o stETH como um *Rebase Token*, enquanto os equivalentes compostos ou pares representam abordagens variadas (Atende o Objetivo Específico 3).
2. **Desmistificação da "Garantia Total" do Staking (Objetivos 2 e 4):** A pesquisa de Gogol *et al.* fornece dados empíricos de que o *depeg risk* não é instantaneamente retificável e comprova que investir via Lido DAO expõe o usuário a perigos comportamentais. Mostraremos no TCC que, em picos de estresse sistêmico, o arbitrador (entidade que assegura a paridade de liquidez) perde a força contra a manada.
3. **Descentralização como Prêmio Financeiro:** A resposta de precificação aos colapsos de 2022 sublinha como os investidores podem pagar mais por vetores de descentralização e resistência à censura do protocolo, uma vantagem competitiva do "Staking Descentralizado via DAO" contra provedores centralizados institucionais (Coinbase/Binance).
