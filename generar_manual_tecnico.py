"""
Generador del Manual Tecnico de CONDOSYS (PDF).

Uso:
    .venv\\Scripts\\python.exe generar_manual_tecnico.py

Produce: MANUAL_TECNICO_CONDOSYS.pdf
"""

import os
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

# ---------------------------------------------------------------------------
# Fuentes
# ---------------------------------------------------------------------------

F = "SegoeUI"
FB = "SegoeUI-Bold"
FI = "SegoeUI-Italic"
FBI = "SegoeUI-BoldItalic"
FL = "SegoeUI-Light"
FM = "Consolas"
FMB = "Consolas-Bold"

FONTS = r"C:\Windows\Fonts"


def _register():
    faces = {
        F: "segoeui.ttf",
        FB: "segoeuib.ttf",
        FI: "segoeuii.ttf",
        FBI: "segoeuiz.ttf",
        FL: "segoeuil.ttf",
        FM: "consola.ttf",
        FMB: "consolab.ttf",
    }
    for name, filename in faces.items():
        path = os.path.join(FONTS, filename)
        if not os.path.exists(path):
            raise SystemExit("Falta la fuente %s" % path)
        pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily(
        F, normal=F, bold=FB, italic=FI, boldItalic=FBI
    )


_register()

# ---------------------------------------------------------------------------
# Paleta (tomada de static/css/variables.css)
# ---------------------------------------------------------------------------

GREEN_900 = colors.HexColor("#163D1F")
GREEN_700 = colors.HexColor("#308242")
GREEN_500 = colors.HexColor("#43B755")
GREEN_100 = colors.HexColor("#C5E9CD")
GREEN_50 = colors.HexColor("#ECF8EF")
RED_500 = colors.HexColor("#EE443F")
RED_50 = colors.HexColor("#FDECEC")
YELLOW_500 = colors.HexColor("#FFAA00")
YELLOW_50 = colors.HexColor("#FFF7E6")
BLUE_500 = colors.HexColor("#0095FF")
BLUE_50 = colors.HexColor("#E6F4FF")
BLACK_500 = colors.HexColor("#11120D")
BLACK_300 = colors.HexColor("#60605D")
BLACK_100 = colors.HexColor("#B5B6B4")
WHITE_600 = colors.HexColor("#DCDCDC")
WHITE_200 = colors.HexColor("#F9F9F9")
CODE_BG = colors.HexColor("#F4F6F4")
LINE = colors.HexColor("#D8E4DA")


def esc(value):
    """Escapa texto para el mini-lenguaje de marcado de ReportLab."""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline(value):
    """Escapa y convierte \\n en <br/>."""
    return esc(value).replace("\n", "<br/>")


# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------

styles = getSampleStyleSheet()

S = {}

S["cover_kicker"] = ParagraphStyle(
    "cover_kicker",
    parent=styles["Normal"],
    fontName=FB,
    fontSize=10.5,
    leading=14,
    textColor=GREEN_700,
    alignment=TA_CENTER,
    spaceAfter=10,
)

S["cover_title"] = ParagraphStyle(
    "cover_title",
    parent=styles["Title"],
    fontName=FB,
    fontSize=30,
    leading=35,
    textColor=GREEN_900,
    alignment=TA_CENTER,
    spaceAfter=6,
)

S["cover_sub"] = ParagraphStyle(
    "cover_sub",
    parent=styles["Normal"],
    fontName=FL,
    fontSize=15,
    leading=21,
    textColor=BLACK_300,
    alignment=TA_CENTER,
    spaceAfter=26,
)

S["cover_meta"] = ParagraphStyle(
    "cover_meta",
    parent=styles["Normal"],
    fontName=F,
    fontSize=10,
    leading=16,
    textColor=BLACK_300,
    alignment=TA_CENTER,
)

S["h1"] = ParagraphStyle(
    "h1",
    parent=styles["Heading1"],
    fontName=FB,
    fontSize=19,
    leading=23,
    textColor=GREEN_900,
    spaceBefore=2,
    spaceAfter=11,
)

S["h2"] = ParagraphStyle(
    "h2",
    parent=styles["Heading2"],
    fontName=FB,
    fontSize=14,
    leading=18,
    textColor=GREEN_700,
    spaceBefore=15,
    spaceAfter=7,
)

S["h3"] = ParagraphStyle(
    "h3",
    parent=styles["Heading3"],
    fontName=FB,
    fontSize=11.5,
    leading=15,
    textColor=BLACK_500,
    spaceBefore=11,
    spaceAfter=5,
)

S["body"] = ParagraphStyle(
    "body",
    parent=styles["BodyText"],
    fontName=F,
    fontSize=9.5,
    leading=14.2,
    textColor=BLACK_500,
    alignment=TA_JUSTIFY,
    spaceAfter=7,
)

S["bullet"] = ParagraphStyle(
    "bullet",
    parent=S["body"],
    leftIndent=14,
    bulletIndent=4,
    spaceAfter=3.5,
)

S["bullet2"] = ParagraphStyle(
    "bullet2",
    parent=S["body"],
    leftIndent=28,
    bulletIndent=18,
    spaceAfter=3,
)

S["cell"] = ParagraphStyle(
    "cell",
    parent=styles["Normal"],
    fontName=F,
    fontSize=8,
    leading=10.6,
    textColor=BLACK_500,
)

S["cell_b"] = ParagraphStyle(
    "cell_b",
    parent=S["cell"],
    fontName=FB,
)

S["cell_mono"] = ParagraphStyle(
    "cell_mono",
    parent=S["cell"],
    fontName=FM,
    fontSize=7.4,
    leading=10,
)

S["cell_head"] = ParagraphStyle(
    "cell_head",
    parent=S["cell"],
    fontName=FB,
    textColor=colors.white,
    fontSize=8.2,
    leading=10.8,
)

S["code"] = ParagraphStyle(
    "code",
    parent=styles["Code"],
    fontName=FM,
    fontSize=7.6,
    leading=10.4,
    textColor=colors.HexColor("#1C2E20"),
    backColor=CODE_BG,
    borderPadding=7,
    borderWidth=0,
    spaceBefore=5,
    spaceAfter=9,
    wordWrap="CJK",
)

S["caption"] = ParagraphStyle(
    "caption",
    parent=styles["Normal"],
    fontName=FI,
    fontSize=8,
    leading=11,
    textColor=BLACK_300,
    spaceBefore=2,
    spaceAfter=9,
)

S["note"] = ParagraphStyle(
    "note",
    parent=S["body"],
    fontName=F,
    fontSize=9,
    leading=13.2,
)

S["toc1"] = ParagraphStyle(
    "toc1",
    parent=styles["Normal"],
    fontName=FB,
    fontSize=10,
    leading=19,
    textColor=GREEN_900,
    spaceBefore=7,
)

S["toc2"] = ParagraphStyle(
    "toc2",
    parent=styles["Normal"],
    fontName=F,
    fontSize=9,
    leading=14,
    textColor=BLACK_500,
    leftIndent=14,
)


# ---------------------------------------------------------------------------
# Flowables de ayuda
# ---------------------------------------------------------------------------


class HRule(Flowable):
    """Linea horizontal fina."""

    def __init__(self, width, color=LINE, thickness=0.7, space=4):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness
        self.height = thickness + space

    def wrap(self, aw, ah):
        self.width = aw
        return (aw, self.height)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space, self.width, self.space)


class Callout(Flowable):
    """Caja de aviso con barra lateral de color."""

    PALETTES = {
        "info": (BLUE_500, BLUE_50),
        "ok": (GREEN_500, GREEN_50),
        "warn": (YELLOW_500, YELLOW_50),
        "risk": (RED_500, RED_50),
    }
    LABELS = {"info": "NOTA", "ok": "BUENA PRACTICA", "warn": "ATENCION", "risk": "RIESGO"}

    def __init__(self, text, kind="info", width=400, style_name="note"):
        Flowable.__init__(self)
        self.text = text
        self.kind = kind
        self.width = width
        self.style = S[style_name]
        self.accent, self.bg = self.PALETTES[kind]
        self.label = self.LABELS[kind]

    def wrap(self, aw, ah):
        self.width = aw
        inner = aw - 20
        p = Paragraph(self.text, self.style)
        _, h = p.wrap(inner, ah)
        lab = Paragraph(
            '<font color="%s"><b>%s</b></font>'
            % (self.accent.hexval().replace("0x", "#")[-6:], self.label),
            S["note"],
        )
        _, lh = lab.wrap(inner, 20)
        self.height = h + lh + 16
        return (aw, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.setStrokeColor(self.accent)
        c.setLineWidth(0.5)
        c.rect(0, 0, self.width, self.height, stroke=1, fill=1)
        c.setFillColor(self.accent)
        c.rect(0, 0, 2.4, self.height, stroke=0, fill=1)
        inner = self.width - 20
        y = self.height - 6
        lab = Paragraph(
            '<font color="%s"><b>%s</b></font>'
            % (self.accent.hexval().replace("0x", "#")[-6:], self.label),
            S["note"],
        )
        _, lh = lab.wrap(inner, 20)
        lab.drawOn(c, 10, y - lh)
        y -= lh + 3
        p = Paragraph(self.text, self.style)
        _, h = p.wrap(inner, self.height)
        p.drawOn(c, 10, y - h)


# ---------------------------------------------------------------------------
# Helpers de composicion
# ---------------------------------------------------------------------------


def h1(text):
    return Paragraph(esc(text), S["h1"])


def h2(text):
    return Paragraph(esc(text), S["h2"])


def h3(text):
    return Paragraph(esc(text), S["h3"])


def p(text):
    return Paragraph(inline(text), S["body"])


def bullets(items, level=0):
    st = S["bullet"] if level == 0 else S["bullet2"]
    return [
        Paragraph(inline(t), st, bulletText="\u25aa" if level == 0 else "\u2013")
        for t in items
    ]


def code(text):
    return Preformatted(text.strip("\n"), S["code"])


def caption(text):
    return Paragraph(inline(text), S["caption"])


def table(rows, widths, header=True, align=None, mono_cols=(), zebra=True):
    """rows: lista de listas de str. La primera fila es encabezado si header."""
    data = []
    for r, row in enumerate(rows):
        out = []
        for c, val in enumerate(row):
            if r == 0 and header:
                st = S["cell_head"]
            elif c in mono_cols:
                st = S["cell_mono"]
            else:
                st = S["cell"]
            out.append(Paragraph(inline(val) if val else "", st))
        data.append(out)

    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), GREEN_900),
            ("TOPPADDING", (0, 0), (-1, 0), 6),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ]
    if zebra:
        start = 1 if header else 0
        for i in range(start, len(data)):
            if (i - start) % 2 == 1:
                style.append(("BACKGROUND", (0, i), (-1, i), GREEN_50))
    if align:
        for col, a in align.items():
            style.append(("ALIGN", (col, 0), (col, -1), a))
    t.setStyle(TableStyle(style))
    return t


def kv(rows, w1=4.2 * cm):
    """Tabla clave/valor de dos columnas."""
    return table(
        [["Clave", "Descripcion"]] + rows,
        [w1, 16.6 * cm - w1],
        mono_cols=(0,),
    )


# ---------------------------------------------------------------------------
# Plantilla del documento
# ---------------------------------------------------------------------------

PW, PH = LETTER
ML = 2.0 * cm
MR = 2.0 * cm
MT = 2.1 * cm
MB = 1.9 * cm
CW = PW - ML - MR

DOC_TITLE = "Manual Tecnico CONDOSYS"


class ManualDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, **kw)
        frame_cover = Frame(ML, MB, CW, PH - MB - 1.4 * cm, id="cover")
        frame = Frame(ML, MB, CW, PH - MT - MB, id="main")
        self.addPageTemplates(
            [
                PageTemplate(id="Cover", frames=[frame_cover], onPage=self._cover_page),
                PageTemplate(id="Main", frames=[frame], onPage=self._main_page),
            ]
        )
        self._toc_seq = 0

    def _cover_page(self, canv, doc):
        canv.saveState()
        canv.setFillColor(GREEN_900)
        canv.rect(0, PH - 2.2 * cm, PW, 2.2 * cm, stroke=0, fill=1)
        canv.setFillColor(GREEN_500)
        canv.rect(0, PH - 2.35 * cm, PW, 0.15 * cm, stroke=0, fill=1)
        canv.setFillColor(GREEN_900)
        canv.rect(0, 0, PW, 1.1 * cm, stroke=0, fill=1)
        canv.setFillColor(colors.white)
        canv.setFont(F, 8)
        canv.drawCentredString(
            PW / 2.0, 0.42 * cm, "Documento tecnico interno  -  Uso exclusivo del equipo de desarrollo"
        )
        canv.restoreState()

    def _main_page(self, canv, doc):
        canv.saveState()
        canv.setStrokeColor(LINE)
        canv.setLineWidth(0.6)
        canv.line(ML, PH - MT + 0.55 * cm, PW - MR, PH - MT + 0.55 * cm)
        canv.setFont(F, 7.4)
        canv.setFillColor(BLACK_300)
        canv.drawString(ML, PH - MT + 0.72 * cm, DOC_TITLE)
        canv.drawRightString(PW - MR, PH - MT + 0.72 * cm, "CONDOSYS")
        canv.line(ML, MB - 0.5 * cm, PW - MR, MB - 0.5 * cm)
        canv.setFont(F, 7.4)
        canv.drawString(ML, MB - 0.95 * cm, "Rama de trabajo: desarrollo   -   Commit: 2524680")
        canv.setFont(FB, 8)
        canv.setFillColor(GREEN_700)
        canv.drawRightString(PW - MR, MB - 0.95 * cm, "Pagina %d" % canv.getPageNumber())
        canv.restoreState()

    def afterFlowable(self, flowable):
        if not isinstance(flowable, Paragraph):
            return
        name = flowable.style.name
        if name == "h1":
            level = 0
        elif name == "h2":
            level = 1
        else:
            return
        text = flowable.getPlainText()
        self._toc_seq += 1
        self.notify("TOCEntry", (level, text, self.page))

