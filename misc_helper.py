import pdfplumber

def get_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    pdf = pdfplumber.open(pdf_path)
    page = pdf.pages[0]
    text = page.extract_text()
    pdf.close()

    return text
