# Fichamento: On-Chain Analysis of Smart Contract Dependency Risks on Ethereum

**Referência Bibliográfica:**
JIN, M.; LIU, R.; MONPERRUS, M. *On-Chain Analysis of Smart Contract Dependency Risks on Ethereum*. arXiv preprint arXiv:2503.19548v3, 2025.

---

## 1. Problema de Pesquisa e Escopo
O artigo realiza a maior análise empírica feita até o momento (abrangendo mais de 41 milhões de contratos e 11 bilhões de interações) sobre o ecossistema do Ethereum. O escopo principal é avaliar como as dependências entre os *smart contracts* geram riscos sistêmicos, avaliando o grau de composição de blocos (interdependência), a centralização dos emissores (*deployers*) e, fundamentalmente, a **transparência** dos protocolos de Finanças Descentralizadas (DeFi).

---

## 2. Metodologia
- Utilização da plataforma de *blockchain analytics* Allium para extração de dados brutos (chamadas e transações *on-chain*) desde a gênese até dezembro de 2024.
- Análise de topologia de chamadas inter-contratos, classificando chamadas regulares (`CALL`), chamadas estáticas (`STATICCALL`) e chamadas delegadas (`DELEGATECALL`).
- **Estudos de Caso em Transparência:** Realização de uma verredura comparando a documentação oficial dos protocolos contra a malha real de contratos invocados *on-chain*. O estudo focou especificamente nos protocolos Uniswap e **Lido**.

---

## 3. Principais Resultados (Foco Lido DAO)
*Anota-se que a maioria dos achados gerais sobre a centralização do Ethereum foram omitidos deste fichamento por não pertencerem estritamente ao escopo de liquid staking, focando-se no Estudo de Caso do protocolo Lido (Seção IV-D.2).*

### A Opacidade e o Risco de Contratos Inteligentes
A premissa do DeFi é a transparência ("Don't trust, verify"). Contudo, os autores comprovaram um severo hiato entre o que a Lido DAO documenta oficialmente e o que de fato roda no protocolo.

- **Contratos Não Documentados:** Os autores identificaram que **25 contratos do ecossistema Lido operam nas sombras**, sem estarem devidamente mapeados na documentação de desenvolvimento (Lido Docs).
- **Risco dos *Proxies*:** Desses 25 contratos, 16 são contratos de implementação e 4 são contratos *proxy*. O padrão *proxy* (através do uso do opcode `DELEGATECALL`) permite que o contrato delegue a lógica de execução para outro contrato de implementação, possibilitando "atualizações" (upgradeability). 
- **Vetores de Ataque Sistêmico:** A falta de transparência nesses contratos *proxy* ou implementações marginais configura um risco enorme. Como a lógica pode ser alterada sem visibilidade ampla, falhas críticas nessas dependências (sejam introduzidas por erros de desenvolvimento ou por administradores comprometidos) podem levar a drenagem de fundos massiva ou travamento do sistema.

---

## 4. Implicações para o TCC (Riscos do Liquid Staking)
Este artigo atende ao **Objetivo Específico 3**, fundamentando a seção de **Riscos e Desvantagens** do stETH e da Lido.
A vantagem teórica de participar da governança e lucrar com *liquid staking* possui um preço oculto, quantificado neste artigo como **Risco de Dependência (*Dependency Risk*)**:
1. **Composição Opaca:** A adoção do *liquid staking* expõe o investidor a uma malha de contratos complexos (incluindo validadores externos, oráculos e atualizações de *proxy*). Como os autores provam, os usuários estão enviando seus ETHs para um sistema com falhas de transparência documental.
2. **Desmistificação da Descentralização Absoluta:** Mostraremos que o uso de contratos de *proxy* não documentados centraliza o controle técnico (vetor de centralização) nas mãos de quem detém o controle da atualização daquele *proxy*, mitigando as vantagens originais de resistência à censura da rede Ethereum.
