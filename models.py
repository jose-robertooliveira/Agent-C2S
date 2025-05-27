from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Automovel(Base):
    __tablename__ = "automoveis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    motorizacao = Column(String, nullable=False)
    combustivel = Column(String, nullable=False)
    cor = Column(String, nullable=False)
    quilometragem = Column(Integer, nullable=False)
    num_portas = Column(Integer, nullable=False)
    transmissao = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    placa = Column(String(10), unique=True, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Automovel(marca='{self.marca}', modelo='{self.modelo}', ano={self.ano}, "
            f"cor='{self.cor}', preco={self.preco})>"
        )
