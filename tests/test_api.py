from unittest.mock import patch
from io import BytesIO

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@patch("src.api.endpoints.process_contract_and_store")
@patch("src.api.endpoints.extract_text_from_file")
def test_upload_contract(mock_extract, mock_process, client):
    # Mocking external RAG/LLM behavior
    mock_extract.return_value = "Mocked contract text."
    mock_process.return_value = None

    # Simulating a file upload
    file_content = b"Mock content"
    response = client.post(
        "/upload",
        files={"file": ("test_contract.txt", BytesIO(file_content), "text/plain")}
    )
    
    assert response.status_code == 200
    assert "uploaded and indexed successfully" in response.json()["message"]
    mock_extract.assert_called_once()
    mock_process.assert_called_once()

@patch("src.api.endpoints.query_contract")
def test_ask_question(mock_query, client):
    # Mock the LLM answer
    mock_query.return_value = "This is a mocked answer to your legal question."
    
    response = client.post(
        "/ask",
        json={"query": "What is the term?"}
    )
    
    assert response.status_code == 200
    assert response.json()["answer"] == "This is a mocked answer to your legal question."
    mock_query.assert_called_once_with("What is the term?")
