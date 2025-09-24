# Installeer dependency: pip install reportlab
# Zet het bestand Michiel-cropped.jpg (je profielfoto) in dezelfde map als het script.
# Sla het script op als bijvoorbeeld make_cv.py en run python make_cv.py.
# Het genereert CV_Michiel_Kikkert.pdf in dezelfde map.



# make_cv.py
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Image, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from pathlib import Path

# === Config ===
PHOTO_FILENAME = "Michiel-cropped.jpg"   # zet je foto in dezelfde map als dit script
OUTPUT_PDF = "CV_Michiel_Kikkert.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 1 * cm

# === Styles ===
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="HeadingCustom",
    fontSize=12,
    leading=14,
    spaceAfter=6,
    textColor=colors.HexColor("#1b3b36"),
    fontName="Helvetica-Bold"
))
styles.add(ParagraphStyle(
    name="BodyTextCustom",
    fontSize=10,
    leading=12,
    spaceAfter=6,
    fontName="Helvetica"
))
styles.add(ParagraphStyle(
    name="SmallCustom",
    fontSize=9,
    leading=11,
    spaceAfter=4,
    fontName="Helvetica"
))

# === Content (from user) ===
name_line = "<b>Michiel Kikkert</b>"
contact_lines = [
    "06-1055 1891",
    "michiel@kikkert.nl",
    "Heutinkstraat 34",
    "7512GM, Enschede"
]

profile_text = (
    "Senior Angular ontwikkelaar met ruime ervaring als Development/Team Lead bij enterprise "
    "en (semi)-overheidsinstanties. Neemt graag verantwoordelijkheid en begeleidersrollen (Juniors/stagiaires) "
    "op zich en kan fungeren als technische vraagbaak èn als de schakel tussen product/business owners en ontwikkelaars. "
    "Blijvend op de hoogte van de meest recente ontwikkelingen binnen Angular en is actief in de developer community. "
    "Focus op code kwaliteit, performance, security en toegankelijkheid."
)

skills = [
    "Angular", "WCAG/A11Y", "Cloudflare Workers", "Typescript", "NX", "NgRx", "Testing", "Performance",
    "NestJS", "mySQL", "GraphQL", "MongoDB", "GIT", "Jenkins", "Azure DevOps", "Security",
    "Containers", "CDN", "Accessibility tooling"
]

# Experience in exact order provided by user
jobs = [
    ("Lead Angular developer - Nibud", "Mei 2025 - aug 2025",
     "Complete refactor van onderliggende Nibud bereken tools fundament in meest recente Angular met toepassing van alle huidige Angular best practises. "
     "Technische implementaties van WCAG waaronder contrast, toetsenbord navigatie en volledig door screenreaders te lezen formulieren en context."),
    ("Cloudflare workers voor A/B testing - Mintminds", "Nov 2024 - Mei 2025",
     "Het bouwen van een schaalbare Cloudflare Worker voor het uitvoeren van A/B testing mbv Growthbook. Inzetbaar voor meerdere Mintminds e-commerce klanten."),
    ("Lead Angular Developer - Sociale verzekeringsbank", "Apr 2022 - Okt 2024",
     "Frontend Angular Lead in een groot multi-disciplinair team met als doel het volledig ombouwen van een legacy AngularJS applicatie naar nieuwste Angular. Begeleider van de Juniors."),
    ("Lead angular developer - Nibud", "2012 - 2024",
     "Doorgaande ontwikkeling Nibud bereken tools en onderliggende framework. Preferred supplier."),
    ("Lead angular developer - Asito", "2018 - 2020", ""),
    ("Lead angular developer - Verbond van verzekeraars", "2015 - 2020", ""),
    ("Angular developer - Ministerie van Justitie en veiligheid (JUSTID)", "2016 - 2017", ""),
    ("Webdeveloper - Trimm", "2007 - 2009", "Projecten: NXP, Philips, KPN, SLO, Heineken."),
    ("Principal Technical specialist - Avis Europe (United Kingdom)", "2000 - 2005", "")
]

# === Build left column content (photo, contact, skills) ===
left_flow = []

# Photo
photo_path = Path(PHOTO_FILENAME)
if photo_path.exists():
    # scale photo to 3.4cm
    img = Image(str(photo_path), width=3.4*cm, height=3.4*cm)
    # add a small border effect by packing in a table cell with background - optional
    left_flow.append(img)
else:
    left_flow.append(Paragraph("Profielfoto niet gevonden", styles["SmallCustom"]))

left_flow.append(Spacer(1, 6))
left_flow.append(Paragraph(name_line, styles["BodyTextCustom"]))
for line in contact_lines:
    left_flow.append(Paragraph(line, styles["SmallCustom"]))

left_flow.append(Spacer(1, 10))
left_flow.append(Paragraph("Kennis", styles["HeadingCustom"]))

# Create chips (we'll render them as a small table with colored cells)
chip_rows = []
row = []
max_per_row = 2  # how many chips per row visually (adjust to taste)
for i, s in enumerate(skills):
    p = Paragraph(f"<font color='white'>{s}</font>", styles["SmallCustom"])
    # wrap in a one-cell table to enable background color & padding
    cell_table = Table([[p]], colWidths=None)
    cell_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#4fb48c")),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    row.append(cell_table)
    if (i+1) % max_per_row == 0:
        chip_rows.append(row)
        row = []
if row:
    chip_rows.append(row)

# Add chip rows to left_flow
for r in chip_rows:
    t = Table([r], hAlign="LEFT", style=[("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),6)])
    left_flow.append(t)
    left_flow.append(Spacer(1,4))

# pack left_flow into a keepTogether so layout stays neat
left_block = KeepTogether(left_flow)

# === Build right column content (profile + experience) ===
right_flow = []
right_flow.append(Paragraph("Profiel", styles["HeadingCustom"]))
right_flow.append(Paragraph(profile_text, styles["BodyTextCustom"]))
right_flow.append(Spacer(1,6))
right_flow.append(Paragraph("Ervaring", styles["HeadingCustom"]))

for title, period, desc in jobs:
    # Title line with period
    right_flow.append(Paragraph(f"<b>{title}</b> — {period}", styles["BodyTextCustom"]))
    if desc:
        right_flow.append(Paragraph(desc, styles["SmallCustom"]))
    right_flow.append(Spacer(1,6))

right_block = KeepTogether(right_flow)

# === Compose final two-column table ===
# Left column width ~ 6cm, right column flexible
left_col_w = 6.4 * cm
right_col_w = PAGE_WIDTH - 2*MARGIN - left_col_w

main_table = Table(
    [[left_block, right_block]],
    colWidths=[left_col_w, right_col_w],
    style=[
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),12),
        ("RIGHTPADDING",(0,0),(-1,-1),12),
        ("TOPPADDING",(0,0),(-1,-1),12),
        ("BOTTOMPADDING",(0,0),(-1,-1),12),
    ]
)

# === Document setup ===
doc = BaseDocTemplate(OUTPUT_PDF, pagesize=A4,
                      leftMargin=MARGIN, rightMargin=MARGIN,
                      topMargin=MARGIN, bottomMargin=MARGIN)

frame = Frame(MARGIN, MARGIN, PAGE_WIDTH - 2*MARGIN, PAGE_HEIGHT - 2*MARGIN, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
template = PageTemplate(id="normal", frames=[frame])
doc.addPageTemplates([template])

# Build document
doc.build([main_table])

print(f"PDF gegenereerd: {OUTPUT_PDF}")
