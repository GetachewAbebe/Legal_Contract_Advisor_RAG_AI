import pytest
from src.utils.file_parser import extract_text_from_file

def test_extract_text_from_txt():
    # Test extracting text from a simple text file
    content = b"Hello, this is a test text file."
    result = extract_text_from_file("sample.txt", content)
    assert result == "Hello, this is a test text file."

def test_extract_text_unsupported_format():
    # Test that an unsupported format raises a ValueError
    content = b"fake binary data"
    with pytest.raises(ValueError) as excinfo:
        extract_text_from_file("sample.unknown", content)
    assert "Unsupported file type" in str(excinfo.value)
