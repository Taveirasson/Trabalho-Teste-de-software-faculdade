# #Se o python estiver dando problema colocar o caminho da sua pasta no path abaixo:
import sys, os
caminho = os.getcwd()
sys.path.append(os.path.join(caminho, 'principal'))
sys.path.append(os.path.join(caminho))

import pytest
from unittest.mock import patch, MagicMock
import tkinter as tk
from principal.telas.tela_cadastro_loja import TelaCadastroLoja

@pytest.fixture
def setup_tela():  
    with patch('tkinter.Tk') as mock_tk:  
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance
        tela = TelaCadastroLoja(master=mock_tk_instance)
        tela.grid = MagicMock()

        return tela


@patch('principal.telas.tela_cadastro_loja.conectar_banco')
@patch('principal.telas.tela_cadastro_loja.messagebox.showinfo')
def test_cadastro_loja_correto(mock_showinfo, mock_conectar, setup_tela):
    mock_conn = mock_conectar.return_value.__enter__.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = (0,)

    tela = setup_tela
    tela.nome_loja.insert(0, "Loja do Teste")
    tela.cnpj_loja.insert(0, "84548")  
    tela.uf_loja.insert(0, "SC")
    tela.tipo_loja.insert(0, "Geral")


    tela.cadastrar_loja()

    mock_showinfo.assert_called_with("Sucesso", "Loja cadastrada com sucesso!")

    mock_conn.commit.assert_called_once()

    mock_cursor.execute.assert_any_call("""\n            INSERT INTO Lojas (NOME_LOJA, NU_CNPJ, UF, TIPO_LOJA)\n            VALUES (?, ?, ?, ?)""",(tela.nome_loja.get(), tela.cnpj_loja.get(), tela.uf_loja.get(), tela.tipo_loja.get()))


@patch('principal.telas.tela_cadastro_loja.messagebox.showerror')  
def test_campos_incompletos(mock_showerror,  setup_tela):
    tela = setup_tela

    tela.nome_loja.get = MagicMock(return_value="")
    tela.cnpj_loja.get = MagicMock(return_value="")
    tela.uf_loja.get = MagicMock(return_value="")
    tela.tipo_loja.get = MagicMock(return_value="")
    
    tela.cadastrar_loja()

    mock_showerror.assert_called_with("Erro", "Todos os campos devem ser preenchidos.")
    


@patch('principal.telas.tela_cadastro_loja.conectar_banco')
@patch('principal.telas.tela_cadastro_loja.messagebox.showerror')
def test_cnpj_existente(mock_showerror, mock_conectar, setup_tela):
    mock_conn = mock_conectar.return_value.__enter__.return_value
    mock_cursor = mock_conn.cursor.return_value
    
    mock_cursor.fetchone.return_value = (1,)  

    tela = setup_tela

    tela.nome_loja.get = MagicMock(return_value="Loja Teste")
    tela.cnpj_loja.get = MagicMock(return_value="151515155")   
    tela.uf_loja.get = MagicMock(return_value="SP")
    tela.tipo_loja.get = MagicMock(return_value="Varejo")

    tela.cadastrar_loja()

    mock_showerror.assert_called_with("Erro", "Já existe uma loja com esse CNPJ.")
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_any_call("SELECT COUNT(*) FROM Lojas WHERE NU_CNPJ = ?",("151515155",)
    )