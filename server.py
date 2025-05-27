import socket
import json
from base import SessionLocal
from models import Automovel


def selecionar_carros(filtros: dict) -> list[dict]:
    session = SessionLocal()

    query = session.query(Automovel)

    if "marca" in filtros:
        query = query.filter(Automovel.marca.ilike(f"%{filtros['marca']}%"))
    if "ano" in filtros:
        query = query.filter(Automovel.ano == int(filtros["ano"]))
    if "combustivel" in filtros:
        query = query.filter(Automovel.combustivel.ilike(f"%{filtros['combustivel']}%"))
    if "preco_min" in filtros:
        query = query.filter(Automovel.preco >= float(filtros["preco_min"]))
    if "preco_max" in filtros:
        query = query.filter(Automovel.preco <= float(filtros["preco_max"]))

    carros = query.all()

    """Não havendo nenhum resultado, buscar novamente sem considerar os filtros de preço"""
    if not carros and ("preco_min" in filtros or "preco_max" in filtros):
        query_alternativo = session.query(Automovel)

        if "marca" in filtros:
            query_alternativo = query_alternativo.filter(
                Automovel.marca.ilike(f"%{filtros['marca']}%")
            )
        if "ano" in filtros:
            query_alternativo = query_alternativo.filter(
                Automovel.ano == int(filtros["ano"])
            )
        if "combustivel" in filtros:
            query_alternativo = query_alternativo.filter(
                Automovel.combustivel.ilike(f"%{filtros['combustivel']}%")
            )

        carros = query_alternativo.all()

    session.close()

    return [
        {
            "marca": carro.marca,
            "modelo": carro.modelo,
            "ano": carro.ano,
            "cor": carro.cor,
            "quilometragem": carro.quilometragem,
            "preco": carro.preco,
        }
        for carro in carros
    ]


def start_server(host: str = "127.0.0.1", port: int = 5000) -> None:
    print(f"📡 Servidor MCP iniciado em {host}:{port}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    while True:
        conn, addr = server_socket.accept()
        print(f"📥 Conexão recebida de {addr}")

        data = conn.recv(4096).decode()
        filtros = json.loads(data)

        print(f"📤 Filtros recebidos: {filtros}")
        resultados = selecionar_carros(filtros)

        conn.sendall(json.dumps(resultados, ensure_ascii=False).encode())
        conn.close()


if __name__ == "__main__":
    start_server()
