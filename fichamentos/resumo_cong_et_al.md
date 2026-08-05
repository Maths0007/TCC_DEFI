# Fichamento: The Tokenomics of Staking

**Referência Bibliográfica:**
CONG, L. W.; HE, Z.; TANG, K. *The Tokenomics of Staking*. NBER Working Paper No. 33640, April 2025.

---

## 1. Problema de Pesquisa
O artigo formula um modelo matemático de finanças contínuas no tempo para explicar as dinâmicas de preços e os incentivos de participação no *staking* de criptoativos baseados em PoS (Proof-of-Stake). O foco central é entender como a "Staking Ratio" (a proporção de tokens totais que estão trancados em *staking*) influencia endogenamente o retorno dos investimentos, a adoção da plataforma e as quebras das regras tradicionais de câmbio (como a violação da Paridade Descoberta de Taxas de Juros - UIP).

## 2. Abordagem Metodológica
- É um modelo macro-financeiro baseado em *Continuous-Time PDE (Partial Differential Equations)*. 
- Ele mensura o *trade-off* do usuário que precisa decidir entre manter o token líquido (para conveniência transacional na plataforma) ou travá-lo em *staking* (perdendo liquidez, mas ganhando as recompensas inflacionárias e taxas pagas pelos outros).
- Além do modelo teórico, os autores fazem a maior e mais abrangente regressão cruzada de dados até o momento (analisando 66 tokens stakables entre 2018 e 2022) para provar o fenômeno empírico de "Crypto Carry Premium".

## 3. Principais Resultados e Descobertas
1. **Poder Preditivo da Staking Ratio:** O modelo prova que a "Staking Ratio" funciona como o principal indicador de saúde da rede. Se a Staking Ratio sobe, há uma expectativa matemática de que os preços futuros dos tokens irão apreciar. Isso se deve a um choque negativo na oferta circulante somado ao aumento de "utilidade e segurança" percebida pelos usuários.
2. **A Violação da UIP (Uncovered Interest Rate Parity):** Em mercados cambiais tradicionais (Fiat), quando um país oferece taxas de juros mais altas, sua moeda sofre uma depreciação cambial que anula o ganho estrangeiro. No *staking* de criptomoedas, os autores provam que isso **não acontece**.
3. **Prêmio de "Crypto Carry":** Como a UIP é violada, surge uma tese de investimento infalível chamada "Carry Trade". Operadores ganham prêmios colossais (Sharpe Ratio de 1.60) operando *long* (comprados) nos *yields* altos e *short* (vendidos) nos de *yields* baixos. Os rendimentos nominais das recompensas cobrem mais do que o suficiente qualquer risco de desvalorização do token.

## 4. Implicações Estratégicas para o TCC
*Excelente fonte matemática para o Objetivo 1 (Análise do rendimento de investimento).*
- Este artigo justifica cientificamente **por que** investir em *staking* vale a pena. O fenômeno de "Crypto Carry" mostra que, contrariando a teoria financeira clássica, o LST (como stETH) retém seu alto rendimento não sendo depreciado por ele mesmo, garantindo os retornos compostos reais ao investidor. Podemos usar a equação base de "Staking Ratio" de Cong et al. para balizar a análise do rendimento histórico da Lido.
