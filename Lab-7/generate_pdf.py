from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE   = r"d:\desktop\sem-5\Software engineering\PES1UG24AM231-SE\Lab-7"
SS_DIR = os.path.join(BASE, "screenshots")
OUT    = os.path.join(BASE, "Lab7_FuzzTesting_Submission_PES1UG24AM231.pdf")

screenshots = [
    ("step2_buggy_app_run.png",         "Step 2",  "Running the Buggy Application (pet_boarding.py)",
     "The application is run with valid inputs (dog:5, 2,5,7, 1500|100). "
     "It works correctly for well-formed input but contains hidden bugs that "
     "crash on edge cases such as None, empty strings, or missing separators."),

    ("step4_tests_failing_header.png",  "Step 4a", "Fuzz Tests Running on Buggy Code — Test Collection",
     "Hypothesis collected 3 test cases and began fuzzing all three functions "
     "using random Unicode strings and None values."),

    ("step4_tests_failing_summary.png", "Step 4b", "Fuzz Tests FAILING — Hypothesis Found Bugs",
     "Hypothesis discovered 3 distinct failures in parse_booking, 2 in "
     "stay_average, and 3 in payable_fee. Root causes: AttributeError on None "
     "input, ValueError from missing separator, ZeroDivisionError on empty CSV."),

    ("step5_fixed_app_run.png",         "Step 5",  "Running the Fixed Application (pet_boarding.py)",
     "After hardening all three functions with input validation, the application "
     "continues to work correctly with valid inputs, now also handling invalid "
     "inputs gracefully with descriptive ValueError messages."),

    ("step6_tests_passing.png",         "Step 6",  "Fuzz Tests PASSING on Fixed Code",
     "All 3 Hypothesis fuzz tests pass after the fix. The functions no longer "
     "crash on arbitrary inputs — invalid inputs raise controlled ValueError "
     "exceptions instead of unhandled crashes."),
]

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()
BRAND  = colors.HexColor("#1a73e8")
DARK   = colors.HexColor("#202124")
GREY   = colors.HexColor("#5f6368")
GREEN  = colors.HexColor("#1e8e3e")
RED    = colors.HexColor("#d93025")

title_style = ParagraphStyle("title", parent=styles["Title"],
    fontSize=22, textColor=BRAND, spaceAfter=4, alignment=TA_CENTER, leading=28)
subtitle_style = ParagraphStyle("subtitle", parent=styles["Normal"],
    fontSize=11, textColor=GREY, spaceAfter=2, alignment=TA_CENTER)
h2_style = ParagraphStyle("h2", parent=styles["Heading2"],
    fontSize=13, textColor=BRAND, spaceBefore=14, spaceAfter=4)
label_style = ParagraphStyle("label", parent=styles["Normal"],
    fontSize=11, textColor=DARK, fontName="Helvetica-Bold", spaceAfter=2)
desc_style = ParagraphStyle("desc", parent=styles["Normal"],
    fontSize=9.5, textColor=GREY, spaceAfter=8, leading=14)
body_style  = ParagraphStyle("body", parent=styles["Normal"],
    fontSize=10, textColor=DARK, spaceAfter=6, leading=14)
mono_style  = ParagraphStyle("mono", parent=styles["Code"],
    fontSize=8.5, textColor=DARK, spaceAfter=4, leading=13,
    backColor=colors.HexColor("#f1f3f4"), borderPadding=6)

# ── Page template with footer ───────────────────────────────────────────────────
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(2*cm, 1.2*cm, "Lab 7 — Fuzz Testing  |  PES1UG24AM231  |  Rottela Haritej")
    canvas.drawRightString(A4[0]-2*cm, 1.2*cm, f"Page {doc.page}")
    canvas.restoreState()

# ── Build story ────────────────────────────────────────────────────────────────
story = []
W, H = A4

# ── Cover ──────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 2*cm))
story.append(Paragraph("Lab 7: Fuzz Testing", title_style))
story.append(Paragraph("Input Validation Bugs using Hypothesis", subtitle_style))
story.append(Spacer(1, 0.4*cm))
story.append(HRFlowable(width="100%", thickness=2, color=BRAND))
story.append(Spacer(1, 0.6*cm))

meta = [
    ["Name",    "Rottela Haritej"],
    ["SRN",     "PES1UG24AM231"],
    ["Course",  "Software Engineering"],
    ["Lab",     "Lab 7 — Fuzz Testing"],
    ["Tool",    "Python 3.12 · Hypothesis 6.170 · pytest 9.1"],
    ["Repo",    "github.com/RHaritej/PES1UG24AM231-SE"],
]
meta_table = Table(meta, colWidths=[3.5*cm, 11*cm])
meta_table.setStyle(TableStyle([
    ("FONTNAME",    (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTNAME",    (1,0), (1,-1), "Helvetica"),
    ("FONTSIZE",    (0,0), (-1,-1), 10),
    ("TEXTCOLOR",   (0,0), (0,-1), BRAND),
    ("TEXTCOLOR",   (1,0), (1,-1), DARK),
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.white, colors.HexColor("#f8f9fa")]),
    ("TOPPADDING",  (0,0), (-1,-1), 6),
    ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
]))
story.append(meta_table)
story.append(Spacer(1, 0.8*cm))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dadce0")))

# ── Objective ──────────────────────────────────────────────────────────────────
story.append(Paragraph("Objective", h2_style))
story.append(Paragraph(
    "To explore fuzz testing as a security and quality assurance technique by identifying "
    "and fixing bugs in a Python module (<i>pet_boarding.py</i>) using the "
    "<b>Hypothesis</b> property-based fuzzing library.",
    body_style))

# ── Code Under Test ────────────────────────────────────────────────────────────
story.append(Paragraph("Code Under Test — Buggy Functions", h2_style))
story.append(Paragraph(
    "Three functions were fuzz-tested in <b>pet_boarding.py</b>:", body_style))

funcs = [
    ["Function",         "Purpose",                          "Bug"],
    ["parse_booking()",  "Parses 'pet:days' string",         "Crashes on None / missing ':' / non-numeric days"],
    ["stay_average()",   "Averages CSV stay lengths",        "Crashes on None / empty string / ZeroDivisionError"],
    ["payable_fee()",    "Calculates fee after discount",    "Crashes on None / missing '|' / non-numeric values"],
]
func_table = Table(funcs, colWidths=[4*cm, 5*cm, 7.5*cm])
func_table.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), BRAND),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1),"Helvetica"),
    ("FONTSIZE",     (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#f8f9fa")]),
    ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#dadce0")),
    ("TOPPADDING",   (0,0), (-1,-1), 6),
    ("BOTTOMPADDING",(0,0), (-1,-1), 6),
    ("LEFTPADDING",  (0,0), (-1,-1), 7),
    ("TEXTCOLOR",    (2,1), (2,-1), RED),
]))
story.append(func_table)
story.append(Spacer(1, 0.4*cm))

story.append(PageBreak())

# ── Screenshots ────────────────────────────────────────────────────────────────
story.append(Paragraph("Lab Steps with Screenshots", h2_style))

PAGE_W = W - 4*cm   # usable width

for fname, step, title, description in screenshots:
    path = os.path.join(SS_DIR, fname)

    # Step badge + title
    story.append(Spacer(1, 0.3*cm))
    badge_data = [[Paragraph(f'<font color="white"><b>{step}</b></font>', 
                             ParagraphStyle("b", fontSize=10, alignment=TA_CENTER)),
                   Paragraph(f"<b>{title}</b>", label_style)]]
    badge = Table(badge_data, colWidths=[2.2*cm, PAGE_W-2.2*cm])
    badge.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(0,0), BRAND),
        ("BACKGROUND",   (1,0),(1,0), colors.HexColor("#e8f0fe")),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(badge)

    # Screenshot image
    if os.path.exists(path):
        from PIL import Image as PILImage
        with PILImage.open(path) as pil_img:
            iw, ih = pil_img.size
        ratio = ih / iw
        img_w = PAGE_W
        img_h = img_w * ratio
        max_h = 10*cm
        if img_h > max_h:
            img_h = max_h
            img_w = img_h / ratio
        img = Image(path, width=img_w, height=img_h)
        img.hAlign = "CENTER"
        story.append(img)
    else:
        story.append(Paragraph(f"[Image not found: {fname}]", desc_style))

    # Description
    story.append(Paragraph(f"<i>{description}</i>", desc_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dadce0")))

story.append(PageBreak())

# ── Bugs Found & Fixes ─────────────────────────────────────────────────────────
story.append(Paragraph("Bugs Found and Fixes Applied", h2_style))

bugs = [
    ["Function",         "Input Causing Crash",     "Error Type",         "Fix Applied"],
    ["parse_booking()",  "None",                    "AttributeError",     "Added None check at entry"],
    ["parse_booking()",  "'' (empty string)",        "ValueError",         "Check ':' in text before split"],
    ["parse_booking()",  "':' (no days value)",     "ValueError",         "Validate days with try/float()"],
    ["stay_average()",   "None",                    "AttributeError",     "Added None check at entry"],
    ["stay_average()",   "'' (empty string)",        "ZeroDivisionError",  "Check empty after strip()"],
    ["stay_average()",   "'abc' (non-int CSV)",      "ValueError",         "Validate each part with try/int()"],
    ["payable_fee()",    "None",                    "AttributeError",     "Added None check at entry"],
    ["payable_fee()",    "'' (empty string)",        "ValueError",         "Check '|' in text before split"],
    ["payable_fee()",    "'|' (empty fee/discount)", "ValueError",         "Validate fee/discount with try/float()"],
]
bug_table = Table(bugs, colWidths=[3.8*cm, 4*cm, 3.8*cm, 5*cm])
bug_table.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), DARK),
    ("TEXTCOLOR",    (0,0),(-1,0), colors.white),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1),(-1,-1),"Helvetica"),
    ("FONTSIZE",     (0,0),(-1,-1), 8.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#fce8e6")]),
    ("GRID",         (0,0),(-1,-1), 0.5, colors.HexColor("#dadce0")),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 6),
    ("TEXTCOLOR",    (2,1),(2,-1), RED),
    ("TEXTCOLOR",    (3,1),(3,-1), GREEN),
]))
story.append(bug_table)
story.append(Spacer(1, 0.6*cm))

# ── Conclusion ─────────────────────────────────────────────────────────────────
story.append(Paragraph("Conclusion", h2_style))
story.append(Paragraph(
    "Fuzz testing with <b>Hypothesis</b> successfully uncovered <b>9 distinct crash scenarios</b> "
    "across the three functions in <i>pet_boarding.py</i> — inputs that traditional unit tests "
    "would likely never cover. After applying defensive input validation, all 3 Hypothesis tests "
    "passed, confirming the functions are now robust against arbitrary and malformed inputs. "
    "This lab demonstrates how property-based fuzzing is a powerful complement to conventional "
    "unit testing for improving code quality and security.",
    body_style))

# ── Build PDF ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2.2*cm)

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF saved: {OUT}")
