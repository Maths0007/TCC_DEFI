# Fichamento: Cryptocurrencies and Decentralized Finance (DeFi)

**Referência Bibliográfica:**
MAKAROV, I.; SCHOAR, A. *Cryptocurrencies and Decentralized Finance (DeFi)*. NBER Working Paper 30006, 2022.

---

## 1. Problema de Pesquisa
Este documento fornece um panorama holístico (ponto de vista regulatório e governamental) dos riscos, desafios de conformidade (KYC/AML) e ineficiências sistêmicas causados pela arquitetura não-permissionada das redes baseadas em blockchain e das finanças descentralizadas (DeFi).

## 2. Pontos-Chave (Riscos e Economia)
- **Centralização Endógena (Extração de Rendas):** Diferente da utopia cripto, o artigo prova que o DeFi tende inevitavelmente ao oligopólio. O ganho de escala dos provedores de infraestrutura (como os grandes nós validadores no PoS) e os efeitos de rede levam poucos protocolos a drenarem quase todo o capital da concorrência, o que facilita a cartelização das plataformas para extrair aluguéis (*rents*) maiores sobre os usuários.
- **Limites dos Contratos Inteligentes:** Aponta a inflexibilidade drástica dos *smart contracts*. Como eles operam como "Commitment Devices" inegociáveis ex-post, usuários leigos assinam empréstimos e transferências sem estarem protegidos por proteções contratuais básicas (leis do consumidor, arrependimento), expondo-se a liquidações forçadas hostis.
- **Risco de Oráculos:** Oráculos como a Chainlink ditam os preços no mercado DeFi. Se o custo para subornar (*corromper*) os administradores de um Oráculo for menor que o lucro do roubo decorrente da liquidação sistêmica, a rede cai.
- **Risco Sistêmico vs Regulação:** A alavancagem profunda em empréstimos pseudo-anônimos gera riscos graves de contágio. A conformidade não existe nativamente, e as regulações, para surtirem efeito, teriam que ocorrer nos pontos de on-ramps e off-ramps e focar estritamente nos desenvolvedores dos validadores base.

## 3. Implicações para o TCC
*Material para contexto secundário.*
Será utilizado como base teórica (junto ao artigo de Schär) para estruturar a seção de riscos do protocolo da Lido. As críticas da extração oligopolista de renda e do *Smart Contract Risk* são exatamente as argumentações que utilizaremos ao ponderar as "Vantagens" do Liquid Staking no Objetivo 3.
