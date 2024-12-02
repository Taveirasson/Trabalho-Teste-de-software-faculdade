import pytest
from unittest.mock import patch, MagicMock
from config import conectar_banco

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


def test_conectar_banco_credenciais_invalidas(mock_connect):
    mock_connect.side_effect = Exception("Erro ao conectar ao banco de dados: credenciais inválidas")
    with pytest.raises(Exception, match="Erro ao conectar ao banco de dados: credenciais inválidas"):
        with conectar_banco() as conn:
            # Não deve chegar aqui, pois a exceção será lançada
            pass