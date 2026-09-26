# Fichamento: Your Loss is My Gain: Low Stake Attacks on Liquid Staking Pools

**Referência Bibliográfica:**
YANG, S.; YAISH, A.; GERVAIS, A.; ZHANG, F. *Your Loss is My Gain: Low Stake Attacks on Liquid Staking Pools*. arXiv preprint arXiv:2605.01025v1, 2026.

---

## 1. Problema de Pesquisa e Motivação
A segurança em protocolos de *Proof-of-Stake* sempre assumiu que atacar o consenso não é rentável a não ser que você detenha gigantescas quantias da rede. Os autores quebram esse paradigma apresentando um "Ataque Cruzado" (Cross-Layer Attack). A ideia é: O que acontece se um invasor (um validador concorrente ou cibercriminoso), com pequena participação e nenhum incentivo real na rede base, forjar os eleitores da *Beacon Chain* para danificar os validadores da Lido e lucrar especulando no mercado secundário DeFi sobre a iminente queda do LST (stETH)?

## 2. Metodologia
- **Aprendizado por Reforço Profundo (DRL):** Eles treinaram uma Inteligência Artificial (Maskable PPO) num ambiente simulado do Ethereum que controla "nós" maliciosos. A IA aprende, através da mecânica nativa da *Leader Election* e *Fork Choice* do Ethereum, a causar interrupções, esconder blocos e derrubar maliciosamente a performance dos *nodes* da "vítima" (Lido DAO) sofrendo o mínimo de dano possível.
- **Simulações Empíricas de Desconto (*Depeg*):** Baseados em milhares de dias *on-chain*, os pesquisadores provam a correlação econométrica: a redução da APR do *pool* gera, via sentimento institucional, o "descolamento/desconto" (redução relativa do valor) do LST no mercado.
- **Simulação de Lucro por "Shorting":** Simulações de Monte Carlo mostram matematicamente o lucro esperado ao "vender a descoberto" (fazer um *Short*) os tokens da vítima em protocolos como Aave em antecipação ao golpe de consenso.

## 3. Principais Resultados (Fatos Quantitativos)
1. **Dano Desproporcional:** A inteligência artificial demonstrou que um protocolo rival com apenas 20% do poder da rede, aceitando quase 0 de perdas próprias (cerca de 2.6%), consegue golpear as rentabilidades da vítima em margens desproporcionalmente brutais (8.3% a 10.8%).
2. **Estímulo ao Ataque (Eficiência do *Shorting*):** Os autores mostram empiricamente que ao observar a degradação em performance da rede vítima, um ataque que em base não lucraria nada se sustenta com lucros absurdos via *Lending* (alavancagem em DeFi). Fazendo um depósito e vendendo LST a descoberto, atacantes obtiveram lucros esperados até 11 vezes mais altos que a margem do *staking* honesto.

## 4. Implicações para o TCC (Riscos do Liquid Staking)
*Este artigo é vital para o Objetivo Específico 2 (Riscos de depeg) e Objetivo 4 (Segurança e Estratégia).*
- A pesquisa expõe a maior "brecha de vulnerabilidade econômica" (*economic vulnerability*) do liquid staking. Ao fornecer liquidez transacionável atrelada a uma APR subjacente, o stETH torna-se especulativo. Falsificadores podem não precisar atacar a Aave, basta atacar a mecânica de nós operacionais no nível raiz do Ethereum e monetizar isso apostando na queda do LST.
- Serve como aviso de que as vulnerabilidades do Lido não estão apenas nos seus contratos inteligentes nativos (Smart Contract Risk), mas numa simbiose de vulnerabilidade de consenso de rede ligada com produtos derivados DeFi.
