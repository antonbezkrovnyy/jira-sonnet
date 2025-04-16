import pytest
from app.services.jira import get_jira_client
from unittest.mock import patch

def test_jira_connection():
    with patch('app.services.jira.get_jira_client') as mock_client:
        mock_client.return_value.server_info.return_value = {"version": "8.0.0"}
        client = get_jira_client()
        assert client is not None
        assert client.server_info() is not None