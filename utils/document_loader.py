from docx import Document

def read_docx(file_path):
    """Read and return the text from a .docx file."""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def chunk_text(text, chunk_size=1000):
    """Chunk text into parts of specified size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]