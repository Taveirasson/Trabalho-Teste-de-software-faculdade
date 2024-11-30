#Se o python estiver dando problema colocar o caminho da sua pasta no path abaixo:
import sys
sys.path.append(r'D:/Documents/codigos/a3qualidade/definitiva')

import pytest
from unittest.mock import patch, MagicMock
import tkinter as tk
from principal.telas.tela_consulta_produto import TelaConsultaProduto

@pytest.fixture
def setup_tela():
    root = tk.Tk()
    tela = TelaConsultaProduto(master=root)
    return tela

@patch('principal.telas.tela_consulta_produto.conectar_banco')  
def test_retorno_correto(mock_conectar, setup_tela):
    tela = setup_tela
    
    mock_conn = mock_conectar.return_value.__enter__.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.return_value = [
        (1, "Produto A", "Loja A", 100),
        (2, "Produto B", "Loja B", 150)
    ]

    tela.carregar_produtos()
    items = tela.tree.get_children()
    assert len(items) == 2
    assert tela.tree.item(items[0])['values'] == [1, "Produto A", "Loja A", 100.00]
    assert tela.tree.item(items[1])['values'] == [2, "Produto B", "Loja B", 150.00]
    mock_cursor.execute.assert_any_call(""" 
                SELECT Produtos.ID_PRODUTO, Produtos.NOME_PRODUTO, Lojas.NOME_LOJA, Produtos.PRECO
                FROM Produtos
                LEFT JOIN Lojas ON Produtos.LOJA_DISPONIVEL = Lojas.ID_LOJA
            """)


@patch('principal.telas.tela_consulta_produto.conectar_banco')  
def test_retorno_vazio_dos_produtos(mock_conectar, setup_tela):
    tela = setup_tela
    
    mock_conn = mock_conectar.return_value.__enter__.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.return_value = []

    tela.carregar_produtos()
    items = tela.tree.get_children()
    assert len(items) == 0
    mock_cursor.execute.assert_any_call(""" 
                SELECT Produtos.ID_PRODUTO, Produtos.NOME_PRODUTO, Lojas.NOME_LOJA, Produtos.PRECO
                FROM Produtos
                LEFT JOIN Lojas ON Produtos.LOJA_DISPONIVEL = Lojas.ID_LOJA
            """)