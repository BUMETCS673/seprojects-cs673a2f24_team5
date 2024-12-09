"""
This module is responsible for converting PDF resumes into string text format.
"""

from PyPDF2 import PdfReader


def convert_pdf_to_text(file_path):
    try:
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error processing PDF: {str(e)}"


def parse_resume(file_path):
    return convert_pdf_to_text(file_path)
