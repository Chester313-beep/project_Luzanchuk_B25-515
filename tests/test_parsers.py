import pytest
from unittest.mock import MagicMock, patch, mock_open
from src.parsers.web_parser import WebNewsParser

def test_web_parser():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"title": "p1", "body": "b1"},
        {"title": "p2", "body": "b2"}
    ]
    with patch("requests.get", return_value=mock_response):
        with patch("os.makedirs") as mock_makedirs:
            with patch("builtins.open", mock_open()) as mock_file:
                parser = WebNewsParser(output_file="dummy.jsonl")
                success = parser.fetch_and_save()
                assert success is True
                mock_makedirs.assert_called_once_with('', exist_ok=True)
                mock_file.assert_called_once_with("dummy.jsonl", 'w', encoding='utf-8')
