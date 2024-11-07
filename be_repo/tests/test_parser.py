import os
import pytest
from modules.parser import convert_pdf_to_text


def test_convert_pdf_to_text_success():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "test_resume.pdf")
    result = convert_pdf_to_text(file_path)
    assert "John Doe" in result


def test_convert_pdf_to_text_error():
    result = convert_pdf_to_text("non_existent_file.pdf")
    assert "Error processing PDF" in result
