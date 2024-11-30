#Se o python estiver dando problema colocar o caminho da sua pasta no path abaixo:
import sys
sys.path.append(r'D:/Documents/codigos/a3qualidade/definitiva')

import pytest
from unittest.mock import patch, MagicMock
import tkinter as tk
from principal.telas.tela_cadastro_loja import TelaCadastroLoja

@pytest.fixture
def setup_tela():    
    root = tk.Tk()
    tela = TelaCadastroLoja(master=root)
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

    mock_cursor.execute.assert_any_call("""
            INSERT INTO Lojas (NOME_LOJA, NU_CNPJ, UF, TIPO_LOJA)
            VALUES (?, ?, ?, ?)""",("Loja do Teste", "84548", "SC", "Geral")
    )


@patch('principal.telas.tela_cadastro_loja.conectar_banco')  
@patch('principal.telas.tela_cadastro_loja.messagebox.showerror')  
def test_campos_incompletos(mock_showerror, mock_conectar, setup_tela):
    mock_conn = mock_conectar.return_value.__enter__.return_value
    mock_cursor = mock_conn.cursor.return_value
    #mock_cursor.fetchone.return_value = (0,)  

    tela = setup_tela

    tela.nome_loja.insert(0,"")
    tela.cnpj_loja.insert(0, "") 
    tela.uf_loja.insert(0,"") 
    tela.tipo_loja.insert(0,"") 
    
    tela.cadastrar_loja()

    mock_showerror.assert_called_with("Erro", "Todos os campos devem ser preenchidos.")
    #mock_conn.cursor.assert_called_once()
    


@patch('principal.telas.tela_cadastro_loja.conectar_banco')
@patch('principal.telas.tela_cadastro_loja.messagebox.showerror')
def test_cnpj_existente(mock_showerror, mock_conectar, setup_tela):
    mock_conn = mock_conectar.return_value.__enter__.return_value
    mock_cursor = mock_conn.cursor.return_value
    
    mock_cursor.fetchone.return_value = (1,)  

    tela = setup_tela

    tela.nome_loja.insert(0, "Loja Teste")
    tela.cnpj_loja.insert(0, "151515155")   
    tela.uf_loja.insert(0, "SP")
    tela.tipo_loja.insert(0, "Varejo")

    tela.cadastrar_loja()

    mock_showerror.assert_called_with("Erro", "Já existe uma loja com esse CNPJ.")
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_any_call("SELECT COUNT(*) FROM Lojas WHERE NU_CNPJ = ?",("151515155",)
    )