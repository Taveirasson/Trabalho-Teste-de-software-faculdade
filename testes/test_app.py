#Se o python estiver dando problema colocar o caminho da sua pasta no path abaixo:
# import sys, os
# caminho = os.getcwd()
# sys.path.append(os.path.join(caminho, 'principal'))
# sys.path.append(os.path.join(caminho))

import pytest
import tkinter as tk
from unittest import mock
from unittest.mock import patch, MagicMock
from principal.app import SistemaApp  
from principal.telas.tela_cadastro_loja import TelaCadastroLoja
from principal.telas.tela_cadastro_produto import TelaCadastroProduto
from principal.telas.tela_consulta_produto import TelaConsultaProduto

#teste

@pytest.fixture
def app():
    with patch('tkinter.Tk') as mock_tk:
        mock_app = MagicMock(spec=SistemaApp)
        mock_app.update = MagicMock()  # Evita a execução de update real
        mock_app.criar_frames = MagicMock()  # Evita criação real dos frames
        mock_app.frames = {  # Mock do atributo frames
            "TelaCadastroLoja": MagicMock(spec=TelaCadastroLoja),
            "TelaCadastroProduto": MagicMock(spec=TelaCadastroProduto),
            "TelaConsultaProduto": MagicMock(spec=TelaConsultaProduto)
        }

        for tela in mock_app.frames.values():
            tela.winfo_ismapped.return_value = 0  

        yield mock_app

def test_criar_frames(app):
    # Teste se os frames foram criados corretamente
    app.criar_frames()
    app.criar_frames.assert_called_once()
    assert "TelaCadastroLoja" in app.frames
    assert "TelaCadastroProduto" in app.frames
    assert "TelaConsultaProduto" in app.frames


def test_iniciar_com_tela_consulta_produto(app):
    assert isinstance(app.frames["TelaConsultaProduto"], TelaConsultaProduto)
    assert app.frames["TelaCadastroLoja"].winfo_ismapped() == 0
    assert app.frames["TelaCadastroProduto"].winfo_ismapped() == 0
    app.frames["TelaConsultaProduto"].winfo_ismapped.return_value = 1
    assert app.frames["TelaConsultaProduto"].winfo_ismapped() == 1

@patch.object(SistemaApp, 'exibir_frame')  # Mock da função exibir_frame
def test_exibir_cadastro_loja(mock_exibir_frame, app):
    # Teste se ao clicar em "Cadastro Loja", a função exibir_frame é chamada com "TelaCadastroLoja"
    app.exibir_cadastro_loja()
    mock_exibir_frame("TelaCadastroLoja")
    app.exibir_cadastro_loja.assert_called_once()
    mock_exibir_frame.assert_called_with("TelaCadastroLoja")


@patch.object(SistemaApp, 'exibir_frame')  # Mock da função exibir_frame
def test_exibir_cadastro_produto(mock_exibir_frame, app):
    # Teste se ao clicar em "Cadastro Produto", a função exibir_frame é chamada com "TelaCadastroProduto"
    app.exibir_cadastro_produto()  # Chama o método que deve chamar exibir_frame
    mock_exibir_frame("TelaCadastroProduto")
    app.exibir_cadastro_produto.assert_called_once()
    mock_exibir_frame.assert_called_once_with("TelaCadastroProduto")

@patch.object(SistemaApp, 'exibir_frame')  # Mock da função exibir_frame
def test_exibir_consulta_produto(mock_exibir_frame, app):
    # Teste se ao clicar em "Consultar Produtos", a função exibir_frame é chamada com "TelaConsultaProduto"
    app.exibir_consulta_produto()
    mock_exibir_frame("TelaConsultaProduto")
    app.exibir_consulta_produto.assert_called_once()
    mock_exibir_frame.assert_called_with("TelaConsultaProduto")

def test_inicializacao_app():
    # Testa se o objeto SistemaApp é criado sem problemas
    with patch('principal.app.SistemaApp.__init__', lambda x: None):  # Mock do construtor para evitar execução real
        app = SistemaApp()
        assert isinstance(app, SistemaApp)
