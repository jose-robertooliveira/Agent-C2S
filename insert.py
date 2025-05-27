from faker import Faker
import random
from base import SessionLocal, init_db
from models import Automovel

fake = Faker("pt_BR")

MARCAS_MODELOS = {
    "Toyota": ["Corolla", "Hilux", "Etios", "Yaris"],
    "Honda": ["Civic", "Fit", "HR-V", "City"],
    "Ford": ["Fiesta", "Focus", "Ka", "EcoSport"],
    "Chevrolet": ["Onix", "Cruze", "Spin", "Camaro"],
    "Volkswagen": ["Golf", "Polo", "T-Cross", "Nivus"],
    "Mercedez": ["A-200", "A-35", "GLC Coupé", "Sprinter"],
    "Hyundai": ["HB20", "Creta", "IX35", "Tucson", "Veloster"],
}

COMBUSTIVEIS = ["Gasolina", "Etanol", "Diesel", "Flex", "Eletrico"]
CORES = ["Preto", "Branco", "Prata", "Vermelho", "Azul", "Laranja"]
TRANSMISSOES = ["Manual", "Automatico"]
MOTORIZACOES = ["1.0", "1.3", "1.6", "2.0", "3.0 Turbo", "V6 4.5"]


def criar_carro_fake() -> Automovel:
    marca = random.choice(list(MARCAS_MODELOS.keys()))
    modelo = random.choice(MARCAS_MODELOS[marca])
    return Automovel(
        marca=marca,
        modelo=modelo,
        ano=random.randint(2005, 2023),
        motorizacao=random.choice(MOTORIZACOES),
        combustivel=random.choice(COMBUSTIVEIS),
        cor=random.choice(CORES),
        quilometragem=round(random.uniform(5000, 200000), 2),
        num_portas=random.choice([2, 4]),
        transmissao=random.choice(TRANSMISSOES),
        preco=round(random.uniform(20000, 200000), 2),
        placa=fake.license_plate(),
    )


def main(qtd: int = 125) -> None:
    init_db()
    session = SessionLocal()
    carros = [criar_carro_fake() for _ in range(qtd)]
    session.add_all(carros)
    session.commit()
    session.close()
    print(f"{qtd} carros inseridos na base de dados!")


if __name__ == "__main__":
    main()
