import pytest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk
from principal.telas.tela_cadastro_produto import TelaCadastroProduto

nome_loja_para_teste = "Loja do lucas"

@pytest.fixture
def setup_tela():
    with patch('tkinter.Tk') as mock_tk:  
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance
        with patch.object(TelaCadastroProduto, 'carregar_lojas', return_value=None) as mock_carregar_lojas:
            tela = TelaCadastroProduto(master=mock_tk_instance)
            tela.grid = MagicMock() 
            # tela.loja_combobox = MagicMock(spec=ttk.Combobox)

            return tela

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showerror')  # Mockando a exibição de mensagens de erro
def test_nome_produto_nao_preenchidos(mock_showerror, mock_conectar, setup_tela):
    tela = setup_tela

    tela.nome.get = MagicMock(return_value="")  # Campo vazio
    tela.valor.get = MagicMock(return_value="100")
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.get = MagicMock(return_value=nome_loja_para_teste)
    tela.qtd_estoque.get = MagicMock(return_value="10")
    tela.categoria.get = MagicMock(return_value="Categoria Teste")

    tela.cadastrar_produto()

    # Verifica se a mensagem de erro é exibida
    mock_showerror.assert_called_with("Erro", "O nome do produto é obrigatório.")

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showerror')
def test_valor_produto_invalido(mock_showerror, mock_conectar, setup_tela):
    tela = setup_tela

    tela.nome.get = MagicMock(return_value="Produto Teste")
    tela.valor.get = MagicMock(return_value="abc")  # Valor inválido
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.get = MagicMock(return_value=nome_loja_para_teste)
    tela.qtd_estoque.get = MagicMock(return_value="10")
    tela.categoria.get = MagicMock(return_value="Categoria Teste")
    tela.cadastrar_produto()  # Chamando o método de cadastro
    # Verifica se a mensagem de erro é exibida
    mock_showerror.assert_called_with("Erro", "O valor do produto deve ser um número válido.")

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showerror')
def test_loja_invalida(mock_showerror, mock_conectar, setup_tela):
    tela = setup_tela

    tela.nome.get = MagicMock(return_value="Produto Teste")
    tela.valor.get = MagicMock(return_value="200")  # Valor válido
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.get = MagicMock(return_value="Loja Errada")  # Loja inválida
    tela.qtd_estoque.get = MagicMock(return_value="10")
    tela.categoria.get = MagicMock(return_value="Categoria Teste")
    tela.cadastrar_produto()  
    # Verifica se a mensagem de erro é exibida
    mock_showerror.assert_called_with("Erro", "Selecione uma loja válida.")

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showerror')
def test_quantidade_invalida(mock_showerror, mock_conectar, setup_tela):
    tela = setup_tela

    tela.nome.get = MagicMock(return_value="Produto Teste")
    tela.valor.get = MagicMock(return_value="200")
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.get = MagicMock(return_value=nome_loja_para_teste)
    tela.qtd_estoque.get = MagicMock(return_value="10.1")  # Quantidade inválida (não inteiro)
    tela.categoria.get = MagicMock(return_value="Categoria Teste")

    tela.cadastrar_produto()

    # Verifica se a mensagem de erro é exibida
    mock_showerror.assert_called_with("Erro", "A quantidade de estoque deve ser um número inteiro.")

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showerror')
def test_categoria_invalida(mock_showerror, mock_conectar, setup_tela):
    tela = setup_tela

    tela.nome.get = MagicMock(return_value="Produto Teste")
    tela.valor.get = MagicMock(return_value="200")
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.get = MagicMock(return_value=nome_loja_para_teste)
    tela.qtd_estoque.get = MagicMock(return_value="10")
    tela.categoria.get = MagicMock(return_value="")

    tela.cadastrar_produto()

    # Verifica se a mensagem de erro é exibida
    mock_showerror.assert_called_with("Erro", "A categoria do produto é obrigatória.")

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showinfo')
def test_cadastro_correto(mock_showinfo, mock_conectar, setup_tela):
    mock_conn = mock_conectar.return_value.__enter__.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.return_value = [(1, nome_loja_para_teste, '789562', 'PR', 'Geral')]

    tela = setup_tela

    tela.nome.get = MagicMock(return_value="Produto Teste")
    tela.valor.get = MagicMock(return_value="200")  # Valor válido
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.get = MagicMock(return_value=nome_loja_para_teste)
    tela.qtd_estoque.get = MagicMock(return_value="10")
    tela.categoria.get = MagicMock(return_value="Categoria Teste")
    tela.cadastrar_produto()

    # Verifica se a mensagem de sucesso é exibida
    mock_showinfo.assert_called_with("Sucesso", "Produto cadastrado com sucesso!")

# @patch('principal.telas.tela_cadastro_produto.conectar_banco')
# def test_carregar_lojas(mock_conectar, setup_tela):
#     # Simula o retorno do banco de dados
#     mock_conn = mock_conectar.return_value.__enter__.return_value
#     mock_cursor = mock_conn.cursor.return_value
#     mock_cursor.execute.return_value.fetchall.return_value = [
#         (1, "Loja A", "123456789", "PR", "Geral"),
#         (2, "Loja B", "987654321", "SP", "Varejo"),
#     ]

#     # Setup da tela
#     tela = setup_tela
#     tela.carregar_lojas()  # Chama o método que vai carregar as lojas no combobox

#     # Verifica se o combobox foi preenchido com as lojas
#     assert tela.loja_combobox['values'] == ["Loja A", "Loja B"]  # Verifica se os valores no combobox estão corretos
#     assert tela.lojas_dict == {
#         "Loja A": 1,
#         "Loja B": 2
#     }  # Verifica se o dicionário de lojas está correto