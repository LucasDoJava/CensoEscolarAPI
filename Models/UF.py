from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from helpers.database import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Municipio import Municipio 
    from .Mesorregiao import Mesorregiao
    from .Microrregiao import Microrregiao

class UF(db.Model):
    __tablename__ = "tb_UF"

    codUF: Mapped[int] = mapped_column(primary_key=True)
    UF: Mapped[str] = mapped_column(String)
    nomeEstado: Mapped[str] = mapped_column(String)
    regiao: Mapped[str] = mapped_column(String)

    mesorregioes: Mapped[List["Mesorregiao"]] = relationship("Mesorregiao", back_populates="uf")
    microrregioes: Mapped[List["Microrregiao"]] = relationship("Microrregiao", back_populates="uf")
    municipios: Mapped[List["Municipio"]] = relationship("Municipio", back_populates="uf")
