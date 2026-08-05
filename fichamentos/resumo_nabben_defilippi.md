# Fichamento: Accountability protocols? On-chain dynamics in blockchain governance

**Referência Bibliográfica:**
NABBEN, K.; DE FILIPPI, P. *Accountability protocols? On-chain dynamics in blockchain governance*. Internet Policy Review, v. 13, n. 4, 2024.

---

## 1. Problema de Pesquisa
O artigo examina a dinâmica de *Accountability* (responsabilização e transparência) em sistemas descentralizados, onde a regra do direito (*rule of law*) é substituída pela regra do código (*rule of code*). O estudo de caso adotado é especificamente o protocolo **Lido DAO** e a rede Ethereum. O problema central é: como garantir que o protocolo Lido, controlando quase 30% do mercado de *staking* do Ethereum, não atue de maneira maliciosa ou forme um cartel para dominar a rede subjacente?

## 2. Ameaça ao Ethereum: Cartelização e Falta de Freios e Contrapesos
- **O Risco de Monopólio (Lido Dominance):** A transição do Ethereum para *Proof-of-Stake* gerou uma centralização indesejada em *staking pools*. A Lido administra massivos recursos financeiros e possui apenas um subconjunto limitado de operadores de nós (*node operators*). Se a Lido detiver mais que o teto crítico (33% ou mais), os operadores poderiam, teoricamente, atuar em conluio para fraudar o consenso do Ethereum.
- **Risco de Governança:* O controle sobre as regras do Lido pertence aos detentores do token LDO. Se a DAO decidir agir de má-fé ou for corrompida (por grandes *players* e fundos de venture capital), a rede Ethereum fica à mercê dessa entidade sem que o protocolo Ethereum possua sanções automatizadas nativas para defender os *stakers*.

## 3. A Proposta: *Dual Governance* (Governança Dupla)
Para mitigar os riscos supracitados, o artigo analisa o desenho proposto de *Dual Governance*, que busca ser o mecanismo de freios e contrapesos no formato *rule of code*.
- **Como Funciona:** Em vez do poder ficar concentrado apenas em quem tem o token LDO, a governança dupla dá aos portadores do token **stETH** (os usuários finais e poupadores de *staking*) o **poder de veto**.
- Caso a Lido DAO aprove uma atualização maliciosa (ex: roubo de fundos, alteração de oráculos, cartelização de validadores), portadores de stETH (os detentores do capital real no Ethereum) podem acionar um *Rage Quit* e vetar ou bloquear a mudança. Isso "congela" a governança e permite que os usuários saquem e fujam da rede antes que o pior aconteça.

## 4. Implicações Estratégicas para o TCC
*Este artigo é o pilar qualitativo para os Objetivos Específicos 3 e 4 do TCC (Riscos vs Vantagens da Lido).*
- **Risco Sistêmico (Ponto de Tensão):** Embora o Lido resolva o problema do custo de oportunidade da liquidez (fornecendo o stETH aos usuários), ele cria um vetor de centralização perigoso ("Too Big To Fail" do mundo DeFi). Devemos mencionar no TCC as críticas dos desenvolvedores do Ethereum.
- **Governança como Risco Embutido:** Mostrar que a alternativa de liquid staking embute um risco institucional não presente no staking direto no Ethereum (solo staking). O solo staker responde apenas pelas regras rígidas da *Beacon Chain*. O detentor de stETH responde pelas regras de um DAO gerenciado por terceiros e está sujeito à volatilidade e vulnerabilidade do voto governamental.
