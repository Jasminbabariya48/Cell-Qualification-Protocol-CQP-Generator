import pytest
from docx import Document
from app.generator.template_engine import render_template

def test_render_template(tmp_path):
    template_file = tmp_path / "template.docx"
    Document().save(str(template_file))
    
    output_file = tmp_path / "out.docx"
    data = {"duty_profiles": []}
    
    render_template(str(template_file), data, str(output_file))
    assert output_file.exists()
