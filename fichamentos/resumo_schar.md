# Fichamento: Decentralized Finance: On Blockchain- and Smart Contract-Based Financial Markets

**Referência Bibliográfica:**
SCHÄR, F. *Decentralized Finance: On Blockchain- and Smart Contract-Based Financial Markets*. Federal Reserve Bank of St. Louis Review, v. 103, n. 2, p. 153-174, 2021.

---

## 1. Escopo e Contribuição Principal
Publicado por um banco central (FED), este é um dos principais artigos canônicos de visão macroeconômica do movimento DeFi. O objetivo do artigo é destrinchar a infraestrutura subjacente de Finanças Descentralizadas do Ethereum, traçando um paralelo de como o DeFi copia e melhora os sistemas financeiros tradicionais em termos de acessibilidade, eficiência e composição (composabilidade), mas também carrega grandes riscos operacionais inerentes aos contratos inteligentes.

## 2. A Arquitetura do DeFi (DeFi Stack)
Schär propõe um framework hierárquico em 5 camadas que formam a "pilha" do DeFi. Para o TCC, essa arquitetura é perfeita como *Referencial Teórico*:
1. **Camada de Liquidação (Settlement Layer):** A blockchain base e seu ativo nativo (no nosso caso, o Ethereum e o ETH). Serve como juiz e banco de dados final das transações.
2. **Camada de Ativos (Asset Layer):** Padrões de criação de novos tokens, como os de padrão ERC-20 (ex: stETH). Ativos colateralizados formam o alicerce para empréstimos.
3. **Camada de Protocolos (Protocol Layer):** Onde estão alojados os *smart contracts* de serviços como Exchanges Descentralizadas (Curve) ou Plataformas de Empréstimo (Aave, MakerDAO).
4. **Camada de Aplicação (Application Layer):** Os front-ends das aplicações que o usuário interage diretamente.
5. **Camada de Agregação (Aggregation Layer):** Otimizadores que pegam taxas ou buscam rendimentos entre múltiplos protocolos diferentes.

## 3. Avaliação de Oportunidades e Riscos do DeFi

### Oportunidades
- **Eficiência e Automação:** Execuções baseadas em códigos imutáveis removem o risco de falência da câmara de compensação.
- **Transparência Extrema:** Todas as liquidações e saldos estão publicamente rastreáveis.
- **Composabilidade (Lego de Dinheiro):** É a característica de interoperabilidade máxima; tokens gerados em um protocolo são plugados em outro (o que justifica o incentivo de gerar stETH na Lido e investi-los em plataformas de *Lending* como a Aave para juros compostos).

### Riscos Sistêmicos
- **Risco de Execução de Contratos Inteligentes:** Códigos abertos são alvo de explorações de hackers. Bugs são não rastreáveis antes da implementação.
- **Dependência de Oráculos (Oracle Dependency):** Para os preços de tokens flutuarem corretamente ou colaterais não serem liquidados injustamente, os protocolos dependem da precisão dos dados externos enviados por Oráculos descentralizados (ex. Chainlink).
- **Risco Operacional (Admin Keys):** Alguns protocolos alegam descentralização mas escondem controle de desenvolvimento e de emergência ("pausar fundos") via chaves criptográficas sob domínio de poucos diretores.

## 4. Implicações Estratégicas para o TCC
*Fonte teórica de introdução.*
Sendo de 2021, o documento fala vagamente da tokenização, mas descreve precisamente como a inovação funciona e como a composabilidade se integra em derivativos e dívidas colateralizadas. No TCC, essa base de "riscos de dependência e falhas em Oráculos" servirá para demonstrar de onde o "Smart Contract Risk" e o depeg risk advêm, justificando os riscos de adotar a Lido.
