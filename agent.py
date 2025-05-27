import socket
import json
from rich.console import Console
from rich.table import Table

console = Console()


def agente(texto: str) -> str:
    return input(f"🧑‍💻 {texto} ").strip()


def montar_filtros() -> dict:
    console.print("\n[bold green]Buscando o carro ideal para você![/bold green]\n")

    filtros = {}

    resposta = agente("Você está procurando alguma marca específica?")
    if resposta:
        filtros["marca"] = resposta

    resposta = agente("Algum ano de fabricação em mente?")
    if resposta.isdigit():
        filtros["ano"] = int(resposta)

    resposta = agente(
        "Qual o tipo de combustivel (Gasolina, Etanol, Flex, Diesel, Eletrico)?"
    )
    if resposta:
        filtros["combustivel"] = resposta

    resposta = agente("Qual o valor mínimo que você gostaria de pagar?")
    try:
        filtros["preco_min"] = float(resposta.replace(",", "."))
    except ValueError:
        pass  # Ignora se não for um número

    resposta = agente("E o valor máximo?")
    try:
        filtros["preco_max"] = float(resposta.replace(",", "."))
    except ValueError:
        pass

    console.print("\n[yellow]Buscando carros com os filtros fornecidos...[/yellow]")
    return filtros


def enviando_para_servidor(filtros: dict) -> list[dict]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 5000))
        s.sendall(json.dumps(filtros).encode())
        resposta = s.recv(8192)
        return json.loads(resposta.decode())


def exibir_resultados(carros: list[dict], filtros: dict) -> None:
    if not carros:
        console.print("\n[red]Nenhum carro encontrado com essas definições.[/red]")
        return

    fora_da_faixa = False
    for carro in carros:
        if ("preco_min" in filtros and carro["preco"] < filtros["preco_min"]) or (
            "preco_max" in filtros and carro["preco"] > filtros["preco_max"]
        ):
            fora_da_faixa = True
            break

    if fora_da_faixa:
        console.print(
            "\n[yellow]Não encontramos nenhum nessa faixa de preço, mas temos algumas alternativas:[/yellow]"
        )

    table = Table(title="Carros Encontrados")

    table.add_column("Marca", style="cyan")
    table.add_column("Modelo", style="magenta")
    table.add_column("Ano", justify="center")
    table.add_column("Cor", justify="center")
    table.add_column("KM", justify="right")
    table.add_column("Preço", justify="right")

    for carro in carros:
        table.add_row(
            carro["marca"],
            carro["modelo"],
            str(carro["ano"]),
            carro["cor"],
            f"{carro['quilometragem']:,} km".replace(",", "."),
            f"R$ {carro['preco']:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", "."),
        )

    console.print(table)


if __name__ == "__main__":
    filtros = montar_filtros()
    carros = enviando_para_servidor(filtros)
    exibir_resultados(carros, filtros)
