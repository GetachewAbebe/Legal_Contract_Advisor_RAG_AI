from docx import Document
from logger import logger

def extract_text_from_docx(docx_path):
    """
    Extract text from a Word (`.docx`) file located at `docx_path`.

    Args:
    - docx_path (str): Path to the Word file.

    Returns:
    - list: List of text extracted from the Word document pages.
           Returns an empty list if there is any error during extraction.
    """
    try:
        document = Document(docx_path)
        docx_texts = [paragraph.text for paragraph in document.paragraphs]
        logger.info(f"Extracting text from Word document '{docx_path}' successfully completed")
        return docx_texts
    except Exception as e:
        logger.error(f"Error extracting text from Word document '{docx_path}': {str(e)}")
        return []

if __name__ == "__main__":
    result = extract_text_from_docx("data/Robinson_Advisory.docx")
    print(result)
