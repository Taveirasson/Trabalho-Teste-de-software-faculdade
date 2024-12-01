import pytest
from unittest.mock import patch, MagicMock
import tkinter as tk
from principal.telas.tela_consulta_produto import TelaConsultaProduto

@pytest.fixture
def setup_tela():
    with patch('tkinter.Tk') as mock_tk, patch('tkinter.ttk.Style') as mock_style:
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance
        
        mock_style_instance = MagicMock()
        mock_style.return_value = mock_style_instance
        with patch.object(TelaConsultaProduto, 'carregar_produtos', return_value=None) as mock_carregar_lojas:

            tela = TelaConsultaProduto(master=mock_tk_instance)
            tela.grid = MagicMock()
            return tela


@patch('principal.telas.tela_consulta_produto.conectar_banco')  
def test_retorno_correto(mock_conectar, setup_tela):
    mock_conn = mock_conectar.return_value.__enter__.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.return_value = [
        (1, "Produto A", "Loja A", 100.00),
        (2, "Produto B", "Loja B", 150.00)
    ]
    
    # Obtendo a tela
    tela = setup_tela

    # Mockando o método insert do Treeview para garantir que ele é chamado corretamente
    with patch.object(tela.tree, 'insert') as mock_insert:
        # Chamando o método que carrega os produtos
        tela.carregar_produtos()

        # Verificando se o método insert foi chamado corretamente
        mock_insert.assert_any_call("", "end", values=(1, "Produto A", "Loja A", 100.00))
        mock_insert.assert_any_call("", "end", values=(2, "Produto B", "Loja B", 150.00))

    # Verificando as interações com o banco de dados
    mock_cursor.execute.assert_any_call( """ 
                SELECT Produtos.ID_PRODUTO, Produtos.NOME_PRODUTO, Lojas.NOME_LOJA, Produtos.PRECO
                FROM Produtos
                LEFT JOIN Lojas ON Produtos.LOJA_DISPONIVEL = Lojas.ID_LOJA
            """)


@patch('principal.telas.tela_consulta_produto.conectar_banco')  
def test_retorno_vazio_dos_produtos(mock_conectar, setup_tela):

    mock_conn = mock_conectar.return_value.__enter__.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.return_value = []  # Simulando que não há produtos no banco
    
    # Obtendo a tela
    tela = setup_tela

    # Mockando o método insert do Treeview para garantir que ele não seja chamado
    with patch.object(tela.tree, 'insert') as mock_insert:
        # Chamando o método que carrega os produtos
        tela.carregar_produtos()

        # Verificando que o método insert NÃO foi chamado
        mock_insert.assert_not_called()  # Não deve ser chamado, pois não há produtos

    # Verificando as interações com o banco de dados
    mock_cursor.execute.assert_any_call( """ 
                SELECT Produtos.ID_PRODUTO, Produtos.NOME_PRODUTO, Lojas.NOME_LOJA, Produtos.PRECO
                FROM Produtos
                LEFT JOIN Lojas ON Produtos.LOJA_DISPONIVEL = Lojas.ID_LOJA
            """)

    