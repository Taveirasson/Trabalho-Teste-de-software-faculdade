#Se o python estiver dando problema colocar o caminho da sua pasta no path abaixo:
import sys, os
# sys.path.append(r'D:/Documents/codigos/a3qualidade/definitiva')

import pytest
import tkinter as tk
from unittest import mock
from unittest.mock import patch, MagicMock
from principal.app import SistemaApp  
from principal.telas.tela_cadastro_loja import TelaCadastroLoja
from principal.telas.tela_cadastro_produto import TelaCadastroProduto
from principal.telas.tela_consulta_produto import TelaConsultaProduto
diretorio_base = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do arquivo em execução
sys.path.append(os.path.join(diretorio_base, '..'))

@pytest.fixture
def app():
    # Fixture para inicializar o aplicativo Tkinter
    app = SistemaApp()
    app.update()  # Atualiza a interface gráfica
    return app

def test_criar_frames(app):
    # Teste se os frames foram criados corretamente
    app.criar_frames()
    assert "TelaCadastroLoja" in app.frames
    assert "TelaCadastroProduto" in app.frames
    assert "TelaConsultaProduto" in app.frames

def test_iniciar_com_tela_consulta_produto(app):
    # Teste se a tela de consulta de produtos é a primeira a ser exibida
    assert isinstance(app.frames["TelaConsultaProduto"], TelaConsultaProduto)
    assert app.frames["TelaCadastroLoja"].winfo_ismapped() == 0
    assert app.frames["TelaCadastroProduto"].winfo_ismapped() == 0
    assert app.frames["TelaConsultaProduto"].winfo_ismapped() == 1

@patch.object(SistemaApp, 'exibir_frame')  # Mock da função exibir_frame
def test_exibir_cadastro_loja(mock_exibir_frame, app):
    # Teste se ao clicar em "Cadastro Loja", a função exibir_frame é chamada com "TelaCadastroLoja"
    app.exibir_cadastro_loja()
    mock_exibir_frame.assert_called_with("TelaCadastroLoja")

@patch.object(SistemaApp, 'exibir_frame')  # Mock da função exibir_frame
def test_exibir_cadastro_produto(mock_exibir_frame, app):
    # Teste se ao clicar em "Cadastro Produto", a função exibir_frame é chamada com "TelaCadastroProduto"
    app.exibir_cadastro_produto()
    mock_exibir_frame.assert_called_with("TelaCadastroProduto")

@patch.object(SistemaApp, 'exibir_frame')  # Mock da função exibir_frame
def test_exibir_consulta_produto(mock_exibir_frame, app):
    # Teste se ao clicar em "Consultar Produtos", a função exibir_frame é chamada com "TelaConsultaProduto"
    app.exibir_consulta_produto()
    mock_exibir_frame.assert_called_with("TelaConsultaProduto")

def test_inicializacao_app():
    # Testa se o objeto SistemaApp é criado sem problemas
    app = SistemaApp()
    assert isinstance(app, SistemaApp)
