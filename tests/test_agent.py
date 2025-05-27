import socket
import json
from agent import montar_filtros, enviando_para_servidor, exibir_resultados


"""Teste para montar_filtros simulando inputs"""


def test_montar_filtros(monkeypatch):
    respostas = iter(
        [
            "Mercedez",  # marca
            "2027",  # ano
            "Flex",  # combustível
            "50000",  # preco_min
            "80000",  # preco_max
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(respostas))
    filtros = montar_filtros()

    assert filtros == {
        "marca": "Mercedez",
        "ano": 2027,
        "combustivel": "Flex",
        "preco_min": 50000.0,
        "preco_max": 80000.0,
    }


"""Teste para enviar_para_servidor usando socket mockado"""


def test_enviando_para_servidor(monkeypatch):
    class FakeSocket:
        def __init__(self, *args, **kwargs):
            pass

        def connect(self, address):
            self.connected = True

        def sendall(self, data):
            self.enviado = json.loads(data.decode())

        def recv(self, buffer_size):
            carros_fakes = [
                {
                    "marca": "Mercedez",
                    "modelo": "GL-007",
                    "ano": 2027,
                    "cor": "Preto",
                    "quilometragem": 50000,
                    "preco": 75000.0,
                }
            ]
            return json.dumps(carros_fakes).encode()

        def close(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(socket, "socket", lambda *args, **kwargs: FakeSocket())

    filtros = {"marca": "Mercedez", "ano": 2027, "preco_min": 50000, "preco_max": 80000}

    carros = enviando_para_servidor(filtros)

    assert isinstance(carros, list)
    assert carros[0]["marca"] == "Mercedez"
    assert carros[0]["preco"] == 75000.0


"""Teste básico de exibição só para garantir que não dá erro"""


def test_exibir_resultados(capsys):
    carros = [
        {
            "marca": "Mercedez",
            "modelo": "GL-007",
            "ano": 2027,
            "cor": "Preto",
            "quilometragem": 60000,
            "preco": 65000.0,
        }
    ]
    filtros = {"preco_min": 50000, "preco_max": 80000}

    """Testando se a função roda sem erro, não valida visual na tabela"""
    exibir_resultados(carros, filtros)

    captured = capsys.readouterr()
    assert "Mercedez" in captured.out
    assert "GL-007" in captured.out
