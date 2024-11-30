#Se o python estiver dando problema colocar o caminho da sua pasta no path abaixo:
import sys, os
caminho = os.getcwd()
sys.path.append(os.path.join(caminho, 'principal'))
sys.path.append(os.path.join(caminho))

import pytest
from unittest.mock import patch, MagicMock
import tkinter as tk
from principal.telas.tela_cadastro_produto import TelaCadastroProduto

nome_loja_para_teste = "Loja do lucas"

@pytest.fixture
def setup_tela():
    with patch('tkinter.Tk') as mock_tk:  
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance
        tela = TelaCadastroProduto(master=mock_tk_instance)
        tela.grid = MagicMock()

        # tela.cadastrar_produto = MagicMock()
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
