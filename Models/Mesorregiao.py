from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from helpers.database import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .UF import UF
    from .Municipio import Municipio 
    from .Microrregiao import Microrregiao

class Mesorregiao(db.Model):
    __tablename__ = "tb_Mesorregiao"

    codMesorregiao: Mapped[int] = mapped_column(primary_key=True)
    mesorregiao: Mapped[str] = mapped_column(String)
    codUF: Mapped[int] = mapped_column(ForeignKey("tb_UF.codUF"))
    regiao: Mapped[str] = mapped_column(String)

    uf: Mapped["UF"] = relationship("UF", back_populates="mesorregioes")
    microrregioes: Mapped[List["Microrregiao"]] = relationship("Microrregiao", back_populates="mesorregiao")
    municipios: Mapped[List["Municipio"]] = relationship("Municipio", back_populates="mesorregiao")
