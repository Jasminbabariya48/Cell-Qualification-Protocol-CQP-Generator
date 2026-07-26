import os
import pytest
from app.generator.pdf_parser import parse_datasheet
from reportlab.pdfgen import canvas

def test_parse_datasheet_valid(tmp_path):
    pdf_file = tmp_path / "test.pdf"
    c = canvas.Canvas(str(pdf_file))
    c.drawString(100, 100, "Manufactured by: Dummy Corp")
    c.drawString(100, 80, "Nominal voltage 3.63 V")
    c.save()
    
    metrics = parse_datasheet(str(pdf_file))
    assert metrics.manufacturer_from_datasheet == "Dummy Corp"
    assert metrics.nominal_voltage == "3.63 V"
