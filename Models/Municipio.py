from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from helpers.database import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .UF import UF
    from .Mesorregiao import Mesorregiao
    from .Microrregiao import Microrregiao
    from .Instituicao import Instituicao

class Municipio(db.Model):
    __tablename__ = "tb_Municipio"

    idMunicipio: Mapped[int] = mapped_column(primary_key=True)
    nomeMunicipio: Mapped[str] = mapped_column(String)
    codUF: Mapped[int] = mapped_column(ForeignKey("tb_UF.codUF"))
    regiao: Mapped[str] = mapped_column(String)
    codMesorregiao: Mapped[int] = mapped_column(ForeignKey("tb_Mesorregiao.codMesorregiao"))
    codMicrorregiao: Mapped[int] = mapped_column(ForeignKey("tb_Microrregiao.codMicrorregiao"))

    uf: Mapped["UF"] = relationship("UF", back_populates="municipios")
    mesorregiao: Mapped["Mesorregiao"] = relationship("Mesorregiao", back_populates="municipios")
    microrregiao: Mapped["Microrregiao"] = relationship("Microrregiao", back_populates="municipios")
    instituicoes: Mapped[List["Instituicao"]] = relationship("Instituicao", back_populates="municipio")
