# Fichamento: Leverage Staking with Liquid Staking Derivatives (LSDs)

**Referência:**
XIONG, X.; WANG, Z.; CHEN, X.; KNOTTENBELT, W.; HUTH, M. *Leverage Staking with Liquid Staking Derivatives (LSDs): Opportunities and Risks*. arXiv preprint arXiv:2401.08610v4, 2024.

---

## 1. Problema de Pesquisa e Contexto
O estudo aborda a prática emergente de *leverage staking* (staking alavancado) utilizando *Liquid Staking Derivatives* (LSDs), especificamente o **stETH** do protocolo Lido. Em ecossistemas como o do Ethereum *Proof-of-Stake* (PoS), o uso secundário dos LSDs em plataformas de *lending* (como a Aave) e corretoras descentralizadas (DEX, como a Curve) tem crescido vertiginosamente. O foco dos autores é quantificar o aumento do rendimento (APR) proporcionado por essa recursividade, além de simular e avaliar os riscos associados ao *depeg* do ativo (desvinculação de preço em relação ao ETH) e as consequentes liquidações em cascata (*cascading liquidations*).

## 2. Metodologia
- **Modelagem Analítica:** Os autores formalizam matematicamente as estratégias de *leverage staking* (tanto direto quanto indireto), deduzindo métricas chave como o Fator de Saúde da posição de empréstimo (*Health Factor* - HF), o multiplicador de alavancagem ($LevM$) e o APR.
- **Análise Empírica:** Realizada com dados de *on-chain events* das plataformas Lido, Aave V2 e Curve em um período de 963 dias. Foram identificados 442 endereços ativamente operando posições alavancadas em stETH.
- **Estresse (*Stress Testing*):** Simulações baseadas nas métricas históricas para avaliar a resiliência do sistema diante de eventos de desvalorização severa (usando como parâmetro base a quebra do ecossistema Terra/LUNA em 2022).

## 3. Principais Resultados (Fatos e Dados)
- **Retornos Superiores:** O estudo observou empíricamente que 81.7% das posições de *leverage staking* resultaram em um APR (*Annual Percentage Rate*) líquido significativamente superior ao do *staking* convencional isolado fornecido pela Lido.
- **Efeito de Contágio e Liquidação em Cascata:** Em cenários de desvalorização abrupta do stETH na paridade stETH-ETH, a alavancagem exacerba a pressão de venda. As liquidações forçadas derrubam ainda mais os preços, ativando novos gatilhos de liquidação (ciclo vicioso).
- **Estudo de Caso do Colapso Terra/LUNA (Maio de 2022):** O colapso forçou o retorno maciço de `bETH` (versão *wrapped* do stETH na rede Terra) para o Ethereum, seguido por vendas agressivas de stETH na Curve por entidades como a *Celsius*. Isso gerou um desequilíbrio no *pool* da Curve e causou um *depeg* histórico do stETH, que bateu uma mínima de 0.931 em 18 de maio de 2022.
- **Ação de Desalavancagem (*Deleveraging*):** Os autores mostraram que até mesmo as reações de mitigação dos usuários (ex: queimar as posições para reequilibrar o *Health Factor*) injetam enorme pressão vendedora no mercado, acelerando e aprofundando o choque nos preços e ameaçando a estabilidade de usuários sem alavancagem (*ordinary users*).

## 4. Implicações para o TCC
Este artigo possui **altíssima relevância** para a discussão do trabalho, justificando a sua adoção como literatura *core*:
1. **Riscos do Liquid Staking (Objetivos Específicos 2 e 3):** Provê evidência robusta de que, apesar do atrativo retorno, a dependência em mercados secundários como Curve e Aave introduz vetores de risco adicionais, transformando a volatilidade idiossincrática do protocolo de *staking* num Risco Sistêmico (Liquidação em Cascata).
2. **Volatilidade e *Depeg*:** A análise sobre o *depeg* de maio de 2022 serve como evidência empírica perfeita para suportar a tese de que o stETH **não** é perfeitamente atrelado (1:1) com o ETH no mercado secundário.
3. **Complexidade Estratégica:** A argumentação dos autores deve ser incorporada no capítulo de resultados e discussão, para contrapor as vantagens teóricas do *liquid staking* vs. *staking* direto (solo), visto que a facilidade de composição e financiamento alavancado gera fragilidades (*smart contract risk*, *depeg risk*).
