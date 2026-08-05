import sys
import os
import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # Set slide dimensions to widescreen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    NAVY = RGBColor(0, 43, 73)      # UFCG Navy #002B49
    TEAL = RGBColor(14, 116, 144)   # Accent Teal #0E7490
    DARK_BLUE = RGBColor(15, 23, 42) # Slate Dark #0F172A
    GOLD = RGBColor(217, 119, 6)    # Accent Gold #D97706
    GRAY_BG = RGBColor(248, 250, 252) # Light Gray #F8FAFC
    CARD_BG = RGBColor(255, 255, 255) # Pure White
    TEXT_DARK = RGBColor(30, 41, 59) # Slate 800
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    BORDER_COLOR = RGBColor(226, 232, 240) # Slate 200

    def set_shape_flat(shape, fill_color, border_color=None):
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1)
        else:
            shape.line.fill.background()

    def add_header(slide, title_text, category_text="PROJETO DE TCC - UFCG / CH / UAAC"):
        hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        set_shape_flat(hdr, NAVY)

        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.15), Inches(10), Inches(0.8))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(186, 230, 253)
        
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(255, 255, 255)

        tx_badge = slide.shapes.add_textbox(Inches(10.5), Inches(0.2), Inches(2.3), Inches(0.7))
        tf_b = tx_badge.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.text = "UFCG | UAAC"
        p_b.alignment = PP_ALIGN.RIGHT
        p_b.font.size = Pt(14)
        p_b.font.bold = True
        p_b.font.color.rgb = RGBColor(255, 255, 255)

    def add_footer(slide, current_slide, total_slides=11):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.02))
        set_shape_flat(line, BORDER_COLOR)

        tx = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8), Inches(0.4))
        tf = tx.text_frame
        p = tf.paragraphs[0]
        p.text = "Finanças Descentralizadas: A avaliação do liquid staking via Lido DAO | Matheus Henrique Da Costa"
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED

        tx2 = slide.shapes.add_textbox(Inches(10.5), Inches(7.05), Inches(2.0), Inches(0.4))
        tf2 = tx2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = f"Slide {current_slide} / {total_slides}"
        p2.alignment = PP_ALIGN.RIGHT
        p2.font.size = Pt(9)
        p2.font.bold = True
        p2.font.color.rgb = TEAL

    # ==================== SLIDE 1: COVER (Modelo PDF UFCG/UAAC) ====================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    set_shape_flat(bg1, GRAY_BG)

    hdr_box = slide1.shapes.add_textbox(Inches(1.0), Inches(0.5), Inches(11.333), Inches(1.2))
    tf_hdr = hdr_box.text_frame
    tf_hdr.word_wrap = True
    
    p = tf_hdr.paragraphs[0]
    p.text = "UNIVERSIDADE FEDERAL DE CAMPINA GRANDE"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_hdr.add_paragraph()
    p.text = "CENTRO DE HUMANIDADES"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED

    p = tf_hdr.add_paragraph()
    p.text = "UNIDADE ACADÊMICA DE ADMINISTRAÇÃO E CONTABILIDADE (UAAC)"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL

    card_title = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(2.0), Inches(10.333), Inches(2.4))
    set_shape_flat(card_title, NAVY)

    tb_t = slide1.shapes.add_textbox(Inches(1.8), Inches(2.2), Inches(9.733), Inches(2.0))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    
    p = tf_t.paragraphs[0]
    p.text = "Finanças Descentralizadas: A avaliação do liquid staking via Lido DAO como alternativa de investimento em ativos digitais"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    card_author = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), Inches(4.7), Inches(8.333), Inches(1.8))
    set_shape_flat(card_author, CARD_BG, BORDER_COLOR)

    tb_a = slide1.shapes.add_textbox(Inches(2.7), Inches(4.85), Inches(7.933), Inches(1.5))
    tf_a = tb_a.text_frame
    tf_a.word_wrap = True

    p = tf_a.paragraphs[0]
    p.text = "Autor: Matheus Henrique Da Costa"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK

    p = tf_a.add_paragraph()
    p.text = "Orientador(a): [Nome do Orientador / Orientadora]"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED

    p = tf_a.add_paragraph()
    p.text = "Novembro/2023"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL

    # ==================== HELPER FOR CONTENT SLIDES ====================
    def make_content_slide(slide_num, title, subtitle):
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        set_shape_flat(bg, GRAY_BG)
        add_header(slide, title, f"Slide {slide_num}: {subtitle}")
        add_footer(slide, slide_num, total_slides=11)
        return slide

    def add_card(slide, left, top, width, height, title="", items=None, accent_color=TEAL):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        set_shape_flat(card, CARD_BG, BORDER_COLOR)
        
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.08))
        set_shape_flat(bar, accent_color)

        tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(height - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = NAVY

        if items:
            for idx, item in enumerate(items):
                p = tf.add_paragraph() if (title or idx > 0) else tf.paragraphs[0]
                p.text = f"• {item}"
                p.font.size = Pt(13)
                p.font.color.rgb = TEXT_DARK
                p.space_after = Pt(6)
        return tb

    # ==================== SLIDE 2: INTRODUÇÃO - CONTEXTUALIZAÇÃO ====================
    s2 = make_content_slide(2, "Contextualização: A Evolução do Ethereum & O Staking", "Introdução (1/3)")
    add_card(s2, 0.8, 1.4, 5.7, 5.3, "O Cenário da Rede Ethereum", [
        "Consolidação como principal infraestrutura para contratos inteligentes e Finanças Descentralizadas (SCHÄR, 2021).",
        "A transição 'The Merge' (2022): Mudança do consenso Proof-of-Work (PoW) para Proof-of-Stake (PoS).",
        "Substituição de máquinas com alto consumo energético por bloqueio financeiro de capital (ETHEREUM FOUNDATION, 2022).",
        "A validação de blocos passa a depender do travamento (staking) de moedas Ether (ETH)."
    ], NAVY)
    add_card(s2, 6.8, 1.4, 5.7, 5.3, "A Trava de Liquidez do Staking Direto", [
        "Aporte Mínimo Elevado: Exigência de 32 ETH (aprox. R$ 350 mil+) para rodar um nó validador próprio.",
        "Restrição de Iliquidez: Ativos imobilizados no contrato de depósitos sem utilização concorrente.",
        "Complexidade Técnica: Necessidade de infraestrutura de servidores 24/7 e risco de penalidades operacionais.",
        "Surgimento do Liquid Staking: Protocolos criados para restaurar a liquidez via tokens derivativos representativos."
    ], TEAL)

    # ==================== SLIDE 3: INTRODUÇÃO - PROBLEMÁTICA ====================
    s3 = make_content_slide(3, "Problemática & Pergunta de Pesquisa", "Introdução (2/3)")
    add_card(s3, 0.8, 1.4, 5.7, 5.3, "O Trade-off do Liquid Staking", [
        "Facilidade vs Novas Camadas de Risco: O liquid staking permite qualquer aporte e entrega o token stETH (Lido DAO).",
        "Risco de Base (Liquid Staking Basis): O token derivativo stETH pode negociar com deságio/ágio no mercado secundário (SCHARNOWSKI; JAHANSHAHLOO, 2025).",
        "Exposição a Smart Contracts: Riscos de bugs e exploits nos contratos do protocolo (HARVEY et al., 2021).",
        "Riscos de Consenso: Penalidades de slashing compartilhadas no pool."
    ], GOLD)
    
    rq_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3))
    set_shape_flat(rq_card, NAVY)
    tb_rq = s3.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.5))
    tf_rq = tb_rq.text_frame
    tf_rq.word_wrap = True
    
    p = tf_rq.paragraphs[0]
    p.text = "❓ PERGUNTA DE PESQUISA"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(186, 230, 253)

    p = tf_rq.add_paragraph()
    p.text = "\n“Quais são os retornos, riscos e vantagens do liquid staking via Lido DAO em comparação ao staking direto no Ethereum, com base em dados históricos e métricas públicas?”"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # ==================== SLIDE 4: INTRODUÇÃO - OBJETIVOS & JUSTIFICATIVA ====================
    s4 = make_content_slide(4, "Objetivos do Trabalho & Justificativa", "Introdução (3/3)")
    add_card(s4, 0.8, 1.4, 5.7, 5.3, "🎯 Objetivos da Pesquisa", [
        "OBJETIVO GERAL: Avaliar, com base em dados históricos e métricas públicas, os retornos, riscos e vantagens do liquid staking via Lido DAO como alternativa de investimento.",
        "ESPECÍFICO 1: Levantar o histórico de rendimento (APR/APY) do stETH comparando-o ao staking direto.",
        "ESPECÍFICO 2: Analisar a volatilidade e os riscos de desvinculação (depeg) do stETH em relação ao ETH.",
        "ESPECÍFICO 3: Mapear os riscos e vantagens estruturais em relatórios técnicos e literatura.",
        "ESPECÍFICO 4: Discutir implicações para estratégias de investimento."
    ], NAVY)
    add_card(s4, 6.8, 1.4, 5.7, 5.3, "💡 Justificativa Científica e Prática", [
        "Aceleração do Mercado DeFi: Crescimento exponencial de protocolos de liquidez e restaking (LSDfi).",
        "Lacuna Científica: Escassez de pesquisas quantitativas empíricas testando a paridade stETH/ETH em séries temporais longas.",
        "Relevância para Investidores: Orientação clara sobre custos de oportunidade, taxa de serviço de 10% da Lido e depeg risk.",
        "Sem Coleta Primária: Análise fundamentada em dados públicos auditáveis on-chain."
    ], TEAL)

    # ==================== SLIDE 5: FUNDAMENTAÇÃO - BLOCKCHAIN & SMART CONTRACTS ====================
    s5 = make_content_slide(5, "Infraestrutura Tecnológica: Blockchain & Smart Contracts", "Fundamentação Teórica (1/4)")
    add_card(s5, 0.8, 1.4, 5.7, 5.3, "Livro-Razão Imutável & Turing-Completeness", [
        "Blockchain: Protocolo distribuído e imutável que registra transações sem autoridade central (HARVEY et al., 2021).",
        "Ethereum vs Bitcoin: Enquanto o Bitcoin opera com lógica restrita, o Ethereum é Turing-complete (BUTERIN, 2014).",
        "Ethereum Virtual Machine (EVM): Ambiente global que executa códigos descentralizados escritos em Solidity.",
        "Automação Financeira: Permite a criação de aplicações autônomas sem custodiante tradicional."
    ], NAVY)
    add_card(s5, 6.8, 1.4, 5.7, 5.3, "Smart Contracts & Analogia de Szabo", [
        "Definição de Smart Contracts: Programas autoexecutáveis implantados na blockchain que operam com determinismo (SCHÄR, 2021).",
        "Analogia da Vending Machine: Execução automática assim que as condições pré-programadas são atendidas.",
        "Eliminação de Intermediários: Impossibilidade de interferência externa ou inadimplência fiduciária.",
        "Infraestrutura da Lido: Todo o fluxo do protocolo é gerido por contratos inteligentes auditados (JIN et al., 2025)."
    ], TEAL)

    # ==================== SLIDE 6: FUNDAMENTAÇÃO - DEFI & ECONOMIA DO STAKING ====================
    s6 = make_content_slide(6, "Ecossistema DeFi & Economia do Staking PoS", "Fundamentação Teórica (2/4)")
    add_card(s6, 0.8, 1.4, 5.7, 5.3, "Arquitetura em Camadas DeFi (Schär, 2021)", [
        "Camada de Liquidação (Settlement): Blockchain Ethereum e token Ether (ETH).",
        "Camada de Ativos (Asset Layer): Tokens nativos e derivativos (stETH).",
        "Camada de Protocolos (Protocol Layer): Lido DAO, Uniswap, Curve, Aave.",
        "Componibilidade ('Legos Financeiros'): Integração de tokens derivativos em diferentes protocolos."
    ], NAVY)
    add_card(s6, 6.8, 1.4, 5.7, 5.3, "Fontes de Rendimento no Proof-of-Stake", [
        "1. Camada de Consenso: Emissão inflacionária do protocolo por propor e atestar blocos.",
        "2. Camada de Execução (Priority Fees): Taxas pagas pelos usuários para priorizar transações.",
        "3. MEV (Maximal Extractable Value): Retorno adicional obtido pela reordenação estratégica de transações em blocos.",
        "Compensação pelo Capital: Recompensa pelo travamento de ativos e risco operacional."
    ], GOLD)

    # ==================== SLIDE 7: FUNDAMENTAÇÃO - LIQUID STAKING & LIDO DAO ====================
    s7 = make_content_slide(7, "Liquid Staking & O Protocolo Lido DAO", "Fundamentação Teórica (3/4)")
    add_card(s7, 0.8, 1.4, 5.7, 5.3, "Mecanismo Operacional da Lido DAO", [
        "Pool de Agregação: Permite depósitos de qualquer quantia de ETH, sem limite de 32 ETH (LIDO DAO, 2020).",
        "Emissão de Derivativo: O usuário recebe instantaneamente tokens stETH na proporção 1:1 com o ETH depositado.",
        "Delegação de Validadores: A DAO distribui o stake entre operadores de nós profissionais credenciados.",
        "Taxa de Serviço de 10%: Cobrada sobre os rendimentos gerados (5% operadores e 5% tesouraria da DAO)."
    ], NAVY)
    add_card(s7, 6.8, 1.4, 5.7, 5.3, "Mecânica de Tokens: Rebasing (stETH)", [
        "Mecanismo de Rebase: O saldo de stETH na carteira do investidor ajusta-se diariamente (aumenta) refletindo rendimentos.",
        "Manutenção da Cotação Nominal: Busca manter a proporção nominal de 1 stETH = 1 ETH.",
        "Diferença para Reward-Bearing: Tokens reward-bearing (wstETH) aumentam o preço; o stETH aumenta o saldo de tokens.",
        "Liquidez Secundária: Permite negociação em mercado secundário sem aguardar fila de saque."
    ], TEAL)

    # ==================== SLIDE 8: FUNDAMENTAÇÃO - MATRIZ DE RISCOS ====================
    s8 = make_content_slide(8, "Matriz de Riscos em Liquid Staking", "Fundamentação Teórica (4/4)")
    add_card(s8, 0.8, 1.4, 3.7, 5.3, "1. Risco de Contrato", [
        "Vulnerabilidades em código Solidity (HARVEY et al., 2021).",
        "Auditorias (ChainSecurity) mitigam mas não eliminam riscos.",
        "Imutabilidade impede reversão de perdas."
    ], NAVY)
    add_card(s8, 4.8, 1.4, 3.7, 5.3, "2. Risco de Depeg (Base)", [
        "Desvio de paridade stETH/ETH em mercado secundário (SCHARNOWSKI, 2025).",
        "Sensível a pânicos e choques de liquidez.",
        "Risco de liquidação em posições alavancadas."
    ], GOLD)
    add_card(s8, 8.8, 1.4, 3.7, 5.3, "3. Slashing & Consenso", [
        "Penalidades por inatividade ou conduta maliciosa (double signing).",
        "Riscos correlacionados: falhas simultâneas em múltiplos nós.",
        "Perda de capital no pool (CARRÉ; GABRIEL, 2025)."
    ], TEAL)

    # ==================== SLIDE 9: METODOLOGIA - CLASSIFICAÇÃO & DADOS ====================
    s9 = make_content_slide(9, "Metodologia: Enquadramento & Dados Secundários", "Metodologia (1/2)")
    add_card(s9, 0.8, 1.4, 5.7, 5.3, "Classificação da Pesquisa (ABNT)", [
        "Natureza: Exploratória e Descritiva com abordagem quantitativa e análise documental.",
        "Recorte Temporal: 01 de janeiro de 2022 a 31 de maio de 2026 (capta Pré-Merge, Shapella 2023, Dencun 2024 e maturidade LSDfi).",
        "Isenção de CEP: Utilização exclusiva de dados secundários de acesso público sem seres humanos.",
        "Reprodutibilidade: Scripts em Python documentados e auditáveis no Apêndice."
    ], NAVY)
    add_card(s9, 6.8, 1.4, 5.7, 5.3, "Bases de Dados Secundários On-Chain", [
        "DefiLlama API: Preços stETH/ETH, TVL histórico, Market Share de LSDs e rendimentos históricos (Yields API).",
        "CoinGecko API: Cotações em USD do Ether e volume diário negociado.",
        "Beaconcha.in API: Dados da camada de consenso (total ETH em staking, Staking Ratio).",
        "Dune Analytics: Painéis de validação para taxas brutas do staking direto e distribuição de validadores."
    ], TEAL)

    # ==================== SLIDE 10: METODOLOGIA - PYTHON & FORMULAÇÃO ====================
    s10 = make_content_slide(10, "Esteira de Automação Python & Formulação de Métricas", "Metodologia (2/2)")
    add_card(s10, 0.8, 1.4, 5.7, 5.3, "Esteira de Scripts em Python", [
        "01_coleta_depeg_steth_eth.py: Captura de cotações e cálculo da razão Ratio_t.",
        "02_coleta_preco_eth_usd.py: Coleta de histórico macro de preços ETH/USD.",
        "03_coleta_apr_lido.py: Extração de retorno histórico APR/APY.",
        "04_tratamento_e_metricas.py: Limpeza, unificação temporal (YYYY-MM-DD) e tratamento de ausentes.",
        "05_geracao_graficos_tabelas.py: Compilação estatística e figuras de alta resolução."
    ], NAVY)
    add_card(s10, 6.8, 1.4, 5.7, 5.3, "Formulação Matemática das Métricas", [
        "1. Liquid Staking Basis / Depeg:\n   Depeg_t = [(P_stETH,t - P_ETH,t) / P_ETH,t] * 100",
        "2. Volatilidade Anualizada:\n   σ_anual = σ_diario * √365",
        "3. Rendimento Líquido Comparativo (Spread):\n   ΔYield_t = APR_stETH,t - APR_direto,t",
        "4. Mensuração do custo de oportunidade da taxa de 10% retida pela Lido DAO."
    ], GOLD)

    # ==================== SLIDE 11: REFERÊNCIAS BIBLIOGRÁFICAS ====================
    s11 = make_content_slide(11, "Referências Bibliográficas", "Referências (ABNT)")
    add_card(s11, 0.8, 1.4, 11.733, 5.3, "Fontes Principais Citadas no Projeto", [
        "BINANCE RESEARCH. Data Insights: Liquid Staking and LSDfi Heat Up. Autoria de Keng Ying Sim. 2023.",
        "BUTERIN, Vitalik. Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform. Whitepaper, 2014.",
        "CARRÉ, Sylvain; GABRIEL, Franck. Liquid Staking: When Does It Help? SSRN Electronic Journal, 2025.",
        "CHAINSECURITY. Code Assessment of the LIP-23: Rebase Check Smart Contracts. Public report for Lido, 2024.",
        "ETHEREUM FOUNDATION. A Fusão (The Merge). 2024. Disponível em: https://ethereum.org/pt-br/roadmap/merge/.",
        "HARVEY, Campbell R.; RAMACHANDRAN, Ashwin; SANTORO, Joey. DeFi and the Future of Finance. Hoboken: John Wiley & Sons, 2021.",
        "LIDO. Lido: Ethereum Liquid Staking. Whitepaper. Out. 2020. Disponível em: https://lido.fi/.",
        "SCHARNOWSKI, Stefan; JAHANSHAHLOO, Hossein. The Economics of Liquid Staking Derivatives: Basis Determinants and Price Discovery. Journal of Futures Markets, v. 45, n. 1, p. 91–117, 2025.",
        "SCHÄR, Fabian. Decentralized Finance: On Blockchain- and Smart Contract-Based Financial Markets. Federal Reserve Bank of St. Louis Review, v. 103, n. 2, p. 153–174, 2021."
    ], NAVY)

    output_path = r"c:\Users\mathe\OneDrive\Documents\TCC_DEFI\Apresentacao_TCC_Matheus.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path} (Total 11 slides)")

if __name__ == "__main__":
    create_presentation()
