from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from helpers.database import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .UF import UF
    from .Municipio import Municipio 
    from .Mesorregiao import Mesorregiao

class Microrregiao(db.Model):
    __tablename__ = "tb_Microrregiao"

    codMicrorregiao: Mapped[int] = mapped_column(primary_key=True)
    microrregiao: Mapped[str] = mapped_column(String)
    codMesorregiao: Mapped[int] = mapped_column(ForeignKey("tb_Mesorregiao.codMesorregiao"))
    codUF: Mapped[int] = mapped_column(ForeignKey("tb_UF.codUF"))
    regiao: Mapped[str] = mapped_column(String)

    uf: Mapped["UF"] = relationship("UF", back_populates="microrregioes")
    mesorregiao: Mapped["Mesorregiao"] = relationship("Mesorregiao", back_populates="microrregioes")
    municipios: Mapped[List["Municipio"]] = relationship("Municipio", back_populates="microrregiao")
