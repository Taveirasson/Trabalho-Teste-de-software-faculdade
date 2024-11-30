#Se o python estiver dando problema colocar o caminho da sua pasta no path abaixo:
import sys, os
caminho = os.getcwd()
sys.path.append(os.path.join(caminho, 'principal'))
sys.path.append(os.path.join(caminho))

import pytest
from unittest.mock import patch, MagicMock
from principal.config import conectar_banco

@pytest.fixture
def mock_connect():
    with patch('pyodbc.connect') as mock:
        yield mock

def test_conectar_banco_sucesso(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    with conectar_banco() as conn:
        mock_connect.assert_called_once_with(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=localhost;"
            "Database=DB_Loja;"
            "Trusted_Connection=yes;"
        )
        assert conn == mock_conn
    
    mock_conn.close.assert_called_once()
