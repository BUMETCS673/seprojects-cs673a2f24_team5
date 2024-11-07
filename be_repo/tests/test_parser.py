import pytest
from modules.parser import convert_pdf_to_text


def test_convert_pdf_to_text_success():
    result = convert_pdf_to_text("../tests/test_resume.pdf")
    assert "John Doe" in result


def test_convert_pdf_to_text_error():
    result = convert_pdf_to_text("non_existent_file.pdf")
    assert "Error processing PDF" in result
