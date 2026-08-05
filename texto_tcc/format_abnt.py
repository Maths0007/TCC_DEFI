"""
Script para formatar TCC_Matheus.docx conforme normas ABNT (NBR 14724).
Gera TCC_Matheus_ABNT.docx preservando o original.

v2: corrige bugs de detecção de títulos e aplica formatação mais robusta.
"""

from docx import Document
from docx.shared import Pt, Cm, Twips, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import re

INPUT_FILE = "TCC_Matheus.docx"
OUTPUT_FILE = "TCC_Matheus_ABNT.docx"

# --- ABNT Constants ---
FONT_NAME = "Times New Roman"
FONT_SIZE_BODY = Pt(12)
FONT_SIZE_SMALL = Pt(10)
LINE_SPACING_1_5 = 1.5  # For python-docx MULTIPLE
LINE_SPACING_SINGLE = 1.0
FIRST_LINE_INDENT = Cm(1.25)

# Known section titles in the document (exact or partial match)
KNOWN_TITLES = {
    "Introdução": "primary",
    "Referencial teórico": "primary",
    "Referencial Teórico": "primary",
    "REFERENCIAL TEÓRICO": "primary",
    "Metodologia": "primary",
    "Resultados": "primary",
    "Conclusão": "primary",
    "Considerações Finais": "primary",
    "REFERÊNCIAS": "primary",
    "Referencias": "primary",
    "Referências": "primary",
}


def classify_paragraph(idx, text, style_name, total_paras):
    """
    Classify a paragraph into one of:
    - 'cover': cover page
    - 'title_primary': primary section title
    - 'title_secondary': secondary section title  
    - 'title_tertiary': tertiary section title
    - 'figure_caption': figure/source caption
    - 'reference_title': the "REFERÊNCIAS" heading
    - 'reference_entry': a bibliographic entry
    - 'body': regular body text
    - 'empty': empty paragraph
    - 'list_item': objective/list items
    """
    text_stripped = text.strip()
    
    if not text_stripped:
        return 'empty'
    
    # Cover page: first ~14 paragraphs
    if idx <= 13:
        return 'cover'
    
    # Title paragraph (the TCC title, idx=14)
    if idx == 14:
        return 'cover'
    
    # References section detection - must be "Referências" or "Referencias", NOT "Referencial"
    text_lower = text_stripped.lower()
    if (text_lower.startswith("referências") or text_lower.startswith("referencias")) and "referencial" not in text_lower and len(text_stripped) < 25:
        return 'reference_title'
    
    # Check if it's a numbered section title: "X.Y.Z Title"
    match = re.match(r'^(\d+(?:\.\d+)*)\s+\S', text_stripped)
    if match:
        num = match.group(1)
        # Verify it's a short enough line to be a title (not a paragraph starting with a number)
        # Titles are typically under 100 chars
        if len(text_stripped) < 120:
            dots = num.count('.')
            if dots == 0:
                return 'title_primary'
            elif dots == 1:
                return 'title_secondary'
            elif dots >= 2:
                return 'title_tertiary'
    
    # Check for non-numbered known section titles
    for title, level in KNOWN_TITLES.items():
        if text_stripped.lower() == title.lower() or (
            text_stripped.lower().startswith(title.lower()) and len(text_stripped) < len(title) + 5
        ):
            if level == "primary":
                return 'title_primary'
    
    # Check for "Heading 1" style - these are section titles
    if style_name in ['Heading 1', 'Heading 2', 'Heading 3', 'Título1', 'Ttulo1']:
        if len(text_stripped) < 120:
            return 'title_primary'
    
    # Non-numbered titles like "Infraestrutura Tecnológica: Blockchain, Ethereum"
    # or "O Ecossistema de Finanças Descentralizadas (DeFi)"
    # These are tricky - check for "List Paragraph" style or specific patterns
    if style_name == 'List Paragraph' and len(text_stripped) < 100:
        # Could be a title formatted as list paragraph
        # But also could be the "Referencial teórico" line
        if not text_stripped.startswith(" "):
            return 'title_primary'
    
    # Figure captions
    if text_stripped.startswith("Fonte:") or re.match(r'^Figura\s+\d+', text_stripped):
        return 'figure_caption'
    
    # Objective list items (short items starting with action verbs)
    objective_patterns = [
        "Levantar o histórico",
        "Analisar a volatilidade", 
        "Identificar, a partir",
        "Discutir as implicações",
    ]
    for p in objective_patterns:
        if text_stripped.startswith(p):
            return 'list_item'
    
    # List-like items: "Camada de ...", "Tokens de ...", "Prova de ...", etc.
    list_patterns = [
        r'^Camada de \w+.*\(.*Layer\)',
        r'^Tokens? (de |Reward)',
        r'^Prova de \w+ \(',
        r'^Emissão do Protocolo',
        r'^Gorjetas de Prioridade',
        r'^Valor Máximo extraível',
    ]
    for pat in list_patterns:
        if re.match(pat, text_stripped):
            return 'list_item'
    
    return 'body'


def set_font_for_run(run, font_name=FONT_NAME, font_size=FONT_SIZE_BODY, bold=None, italic=None):
    """Set font properties for a run, including east asian and complex script fonts."""
    run.font.name = font_name
    run.font.size = font_size
    run.font.color.rgb = RGBColor(0, 0, 0)
    
    # Force rFonts on the XML element
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(
            f'<w:rFonts {nsdecls("w")} '
            f'w:ascii="{font_name}" w:hAnsi="{font_name}" '
            f'w:eastAsia="{font_name}" w:cs="{font_name}"/>'
        )
        rPr.insert(0, rFonts)
    else:
        rFonts.set(qn('w:ascii'), font_name)
        rFonts.set(qn('w:hAnsi'), font_name)
        rFonts.set(qn('w:eastAsia'), font_name)
        rFonts.set(qn('w:cs'), font_name)
    
    # Also set szCs to match sz
    szCs = rPr.find(qn('w:szCs'))
    half_points = str(int(font_size.pt * 2))
    if szCs is None:
        szCs = parse_xml(f'<w:szCs {nsdecls("w")} w:val="{half_points}"/>')
        rPr.append(szCs)
    else:
        szCs.set(qn('w:val'), half_points)
    
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic


def set_paragraph_format_abnt(para, alignment, line_spacing_mult, 
                               space_before_pt=0, space_after_pt=0,
                               first_line_indent_cm=None,
                               left_indent_cm=0, right_indent_cm=0):
    """
    Set paragraph formatting robustly by also manipulating XML directly.
    line_spacing_mult: 1.5 => 360 twips, 1.0 => 240 twips in 'auto' lineRule
    """
    pf = para.paragraph_format
    pf.alignment = alignment
    
    # Set spacing via XML to be absolutely sure
    pPr = para._element.get_or_add_pPr()
    
    # Remove existing spacing element
    existing_spacing = pPr.find(qn('w:spacing'))
    if existing_spacing is not None:
        pPr.remove(existing_spacing)
    
    # Calculate line value (in twips for lineRule=auto: 240 = single, 360 = 1.5, 480 = double)
    line_val = str(int(line_spacing_mult * 240))
    before_val = str(int(space_before_pt * 20))  # points to twips
    after_val = str(int(space_after_pt * 20))
    
    spacing = parse_xml(
        f'<w:spacing {nsdecls("w")} '
        f'w:before="{before_val}" w:after="{after_val}" '
        f'w:line="{line_val}" w:lineRule="auto"/>'
    )
    pPr.append(spacing)
    
    # Remove existing indent element
    existing_ind = pPr.find(qn('w:ind'))
    if existing_ind is not None:
        pPr.remove(existing_ind)
    
    # Set indent
    left_twips = str(int(left_indent_cm * 567))  # cm to twips
    right_twips = str(int(right_indent_cm * 567))
    
    if first_line_indent_cm is not None and first_line_indent_cm > 0:
        fi_twips = str(int(first_line_indent_cm * 567))
        ind = parse_xml(
            f'<w:ind {nsdecls("w")} '
            f'w:left="{left_twips}" w:right="{right_twips}" '
            f'w:firstLine="{fi_twips}"/>'
        )
    else:
        ind = parse_xml(
            f'<w:ind {nsdecls("w")} '
            f'w:left="{left_twips}" w:right="{right_twips}" '
            f'w:firstLine="0"/>'
        )
    pPr.append(ind)


def format_cover(para, idx, text):
    """Format cover page paragraphs."""
    text_stripped = text.strip()
    
    if not text_stripped:
        set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.CENTER, 1.5)
        for run in para.runs:
            set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=False)
        return
    
    # Institution lines (1-3)
    if idx <= 3:
        set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.CENTER, 1.5)
        for run in para.runs:
            set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=True)
            run.text = run.text.upper()
        return
    
    # Student name (4)
    if idx == 4:
        set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.CENTER, 1.5)
        for run in para.runs:
            set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=False)
        return
    
    # Title (14)
    if idx == 14:
        set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.CENTER, 1.5)
        for run in para.runs:
            set_font_for_run(run, font_size=Pt(14), bold=True)
        return
    
    # Spacer paragraphs (5-13)
    set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.CENTER, 1.5)
    for run in para.runs:
        set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=False)


def format_title(para, level, text):
    """Format section titles."""
    if level == 'title_primary':
        set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.LEFT, 1.5,
                                   space_before_pt=12, space_after_pt=12)
        for run in para.runs:
            set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=True)
            run.text = run.text.upper()
    
    elif level == 'title_secondary':
        set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.LEFT, 1.5,
                                   space_before_pt=12, space_after_pt=12)
        for run in para.runs:
            set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=True)
    
    elif level == 'title_tertiary':
        set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.LEFT, 1.5,
                                   space_before_pt=12, space_after_pt=12)
        for run in para.runs:
            set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=True)


def format_body(para):
    """Format regular body paragraph."""
    set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.JUSTIFY, 1.5,
                               first_line_indent_cm=1.25)
    for run in para.runs:
        set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=False)


def format_list_item(para):
    """Format list items (no first line indent, but otherwise body formatting)."""
    set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.JUSTIFY, 1.5,
                               first_line_indent_cm=1.25)
    for run in para.runs:
        set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=False)


def format_figure_caption(para):
    """Format figure captions."""
    set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.CENTER, 1.0,
                               space_before_pt=6, space_after_pt=6)
    for run in para.runs:
        set_font_for_run(run, font_size=FONT_SIZE_SMALL, bold=False)


def format_reference_title(para):
    """Format the REFERÊNCIAS heading."""
    set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.CENTER, 1.5,
                               space_before_pt=12, space_after_pt=12)
    for run in para.runs:
        set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=True)
        run.text = "REFERÊNCIAS"


def format_reference_entry(para):
    """Format a bibliographic reference entry."""
    set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.LEFT, 1.0,
                               space_before_pt=0, space_after_pt=6)
    for run in para.runs:
        set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=False)


def format_empty(para):
    """Format empty paragraphs."""
    set_paragraph_format_abnt(para, WD_ALIGN_PARAGRAPH.LEFT, 1.5)
    for run in para.runs:
        set_font_for_run(run, font_size=FONT_SIZE_BODY, bold=False)


def add_page_numbers(doc):
    """Add page numbers to the header (top right, 10pt)."""
    for section in doc.sections:
        header = section.header
        header.is_linked_to_previous = False
        
        for p in header.paragraphs:
            p.clear()
        
        if header.paragraphs:
            para = header.paragraphs[0]
        else:
            para = header.add_paragraph()
        
        para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        run = para.add_run()
        set_font_for_run(run, font_size=FONT_SIZE_SMALL, bold=False)
        fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
        run._element.append(fldChar1)
        
        run2 = para.add_run()
        set_font_for_run(run2, font_size=FONT_SIZE_SMALL, bold=False)
        instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
        run2._element.append(instrText)
        
        run3 = para.add_run()
        set_font_for_run(run3, font_size=FONT_SIZE_SMALL, bold=False)
        fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
        run3._element.append(fldChar2)


def update_styles(doc):
    """Update document styles to ABNT defaults."""
    # Normal style
    style = doc.styles['Normal']
    style.font.name = FONT_NAME
    style.font.size = FONT_SIZE_BODY
    style.font.color.rgb = RGBColor(0, 0, 0)
    
    pf = style.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.first_line_indent = FIRST_LINE_INDENT
    pf.left_indent = Cm(0)
    pf.right_indent = Cm(0)
    
    # Ensure rFonts on Normal style
    rPr = style.element.find(qn('w:rPr'))
    if rPr is not None:
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is not None:
            for attr in ['ascii', 'hAnsi', 'eastAsia', 'cs']:
                rFonts.set(qn(f'w:{attr}'), FONT_NAME)
    
    # Heading styles
    for heading_name in ['Heading 1', 'Heading 2', 'Heading 3']:
        try:
            h_style = doc.styles[heading_name]
            h_style.font.name = FONT_NAME
            h_style.font.size = FONT_SIZE_BODY
            h_style.font.bold = True
            h_style.font.color.rgb = RGBColor(0, 0, 0)
            h_pf = h_style.paragraph_format
            h_pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
            h_pf.line_spacing = 1.5
            h_pf.space_before = Pt(12)
            h_pf.space_after = Pt(12)
            h_pf.first_line_indent = Cm(0)
            h_pf.left_indent = Cm(0)
            h_pf.right_indent = Cm(0)
        except KeyError:
            pass
    
    # List Paragraph style
    try:
        lp_style = doc.styles['List Paragraph']
        lp_pf = lp_style.paragraph_format
        lp_pf.left_indent = Cm(0)
        lp_pf.first_line_indent = FIRST_LINE_INDENT
    except KeyError:
        pass


def main():
    print(f"Opening {INPUT_FILE}...")
    doc = Document(INPUT_FILE)
    
    # Set margins
    print("Setting ABNT margins...")
    for section in doc.sections:
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2)
    
    # Classify and format all paragraphs
    print("Classifying and formatting paragraphs...")
    total_paras = len(doc.paragraphs)
    
    in_references = False
    classifications = {}
    
    # First pass: classify all paragraphs
    for idx, para in enumerate(doc.paragraphs):
        text = para.text
        style_name = para.style.name
        
        if in_references:
            text_stripped = text.strip()
            if text_stripped:
                classifications[idx] = 'reference_entry'
            else:
                classifications[idx] = 'empty'
            continue
        
        cls = classify_paragraph(idx, text, style_name, total_paras)
        classifications[idx] = cls
        
        if cls == 'reference_title':
            in_references = True
    
    # Print classification summary
    print("\nClassification summary:")
    from collections import Counter
    counts = Counter(classifications.values())
    for cls, count in sorted(counts.items()):
        print(f"  {cls}: {count}")
    
    # Print detailed classification for debugging
    print("\nDetailed classification:")
    for idx, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text:
            cls = classifications[idx]
            print(f"  [{idx:3d}] {cls:20s} | {text[:70]}")
    
    # Second pass: apply formatting
    print("\nApplying formatting...")
    for idx, para in enumerate(doc.paragraphs):
        cls = classifications[idx]
        text = para.text
        
        if cls == 'cover':
            format_cover(para, idx, text)
        elif cls in ('title_primary', 'title_secondary', 'title_tertiary'):
            format_title(para, cls, text)
        elif cls == 'reference_title':
            format_reference_title(para)
        elif cls == 'reference_entry':
            format_reference_entry(para)
        elif cls == 'figure_caption':
            format_figure_caption(para)
        elif cls == 'list_item':
            format_list_item(para)
        elif cls == 'body':
            format_body(para)
        elif cls == 'empty':
            format_empty(para)
    
    # Update styles
    print("Updating styles...")
    update_styles(doc)
    
    # Add page numbers
    print("Adding page numbers...")
    add_page_numbers(doc)
    
    # Save
    print(f"\nSaving {OUTPUT_FILE}...")
    doc.save(OUTPUT_FILE)
    print(f"Done! File saved as {OUTPUT_FILE}")
    
    print(f"\n=== ABNT Formatting Applied ===")
    print(f"  Font: {FONT_NAME}, 12pt (10pt for captions/page numbers)")
    print(f"  Line spacing: 1.5 (body/titles), 1.0 (references/captions)")
    print(f"  Margins: top/left 3cm, bottom/right 2cm")
    print(f"  First line indent: 1.25cm (body paragraphs)")
    print(f"  Titles: uppercase bold (primary), bold (secondary/tertiary)")
    print(f"  References: left-aligned, single spacing, ABNT format")
    print(f"  Page numbers: top right, 10pt")


if __name__ == "__main__":
    main()
