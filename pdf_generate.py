import os
import json
import html
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
import pandas as pd
from docx import Document
import markdown

def txt_to_pdf(inp, out):
    c = canvas.Canvas(out, pagesize=A4)
    y = 800
    for line in open(inp, "r", encoding="utf-8"):
        c.drawString(50, y, line.strip())
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()

def img_to_pdf(inp, out):
    Image.open(inp).convert("RGB").save(out)

def docx_to_pdf(inp, out):
    c = canvas.Canvas(out, pagesize=A4)
    y = 800
    doc = Document(inp)
    for p in doc.paragraphs:
        c.drawString(50, y, p.text)
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()

def csv_to_pdf(inp, out):
    df = pd.read_csv(inp)
    c = canvas.Canvas(out, pagesize=A4)
    y = 800
    for row in df.values:
        c.drawString(50, y, " | ".join(map(str, row)))
        y -= 20
    c.save()

def md_to_pdf(inp, out):
    text = markdown.markdown(open(inp).read())
    text = text.replace("<p>", "").replace("</p>", "").split("<br>")
    c = canvas.Canvas(out, pagesize=A4)
    y = 800
    for line in text:
        c.drawString(50, y, line)
        y -= 20
    c.save()


def ipynb_to_pdf(inp, out):
    with open(inp, "r", encoding="utf-8") as f:
        nb = json.load(f)

    c = canvas.Canvas(out, pagesize=A4)
    y = 800

    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            text = "".join(cell.get("source", []))
            for line in text.split("\n"):
                c.drawString(50, y, line)
                y -= 20
                if y < 50:
                    c.showPage()
                    y = 800

        elif cell.get("cell_type") == "code":
            code = "".join(cell.get("source", []))
            safe = html.escape(code)
            for line in safe.split("\n"):
                c.drawString(50, y, "Code: " + line)
                y -= 20
                if y < 50:
                    c.showPage()
                    y = 800

    c.save()


def convert():
    file = input("Enter input file path: ")
    ext = os.path.splitext(file)[1].lower()
    output = os.path.splitext(file)[0] + ".pdf"

    if ext == ".txt":
        txt_to_pdf(file, output)
    elif ext in [".jpg", ".jpeg", ".png"]:
        img_to_pdf(file, output)
    elif ext == ".docx":
        docx_to_pdf(file, output)
    elif ext == ".csv":
        csv_to_pdf(file, output)
    elif ext == ".md":
        md_to_pdf(file, output)
    elif ext == ".ipynb":      
        ipynb_to_pdf(file, output)
    else:
        print("❌ Unsupported format!")
        return

    print(f"\n✔ INPUT:  {file}")
    print(f"✔ OUTPUT: {output}")
    print("\nPDF Successfully Created! ")

convert()

