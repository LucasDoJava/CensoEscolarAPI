from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from helpers.database import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Municipio import Municipio

class Instituicao(db.Model):
    __tablename__ = "tb_instituicao"

    regiao: Mapped[str] = mapped_column(String)
    codRegiao: Mapped[int] = mapped_column(Integer)
    UF: Mapped[str] = mapped_column(String)
    codUF: Mapped[int] = mapped_column(Integer)
    municipio: Mapped[str] = mapped_column(String)
    codMunicipio: Mapped[int] = mapped_column(ForeignKey("tb_Municipio.idMunicipio"))
    entidade: Mapped[str] = mapped_column(String)
    codEntidade: Mapped[int] = mapped_column(Integer)
    matriculas_base: Mapped[int] = mapped_column(Integer)
    ano: Mapped[int] = mapped_column(Integer)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    __mapper_args__ = {
        "primary_key": [codEntidade, ano]
    }

    municipio_obj: Mapped["Municipio"] = relationship("Municipio", back_populates="instituicoes")
