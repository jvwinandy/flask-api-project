import datetime
import json

from sqlalchemy.orm import Mapped, mapped_column
import flask_api.db.database as db
from flask_api.db.models.serializer import Serializer


class Demanda(db.Base, Serializer):
    __tablename__ = "Demandas"

    demanda_id: Mapped[int] = mapped_column(primary_key=True)
    razao_social: Mapped[str] = mapped_column(nullable=False)
    ans: Mapped[int] = mapped_column(nullable=True)
    beneficiarios: Mapped[int] = mapped_column(nullable=True)
    data_atendimento_demanda: Mapped[datetime.datetime] = mapped_column(nullable=True)
    classificacao_demanda: Mapped[str] = mapped_column(nullable=True)
    natureza_demanda: Mapped[str] = mapped_column(nullable=True)
    subtema_demanda: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<Demanda {self.demanda_id} - {self.ans} - {self.classificacao_demanda}>"

    def __str__(self):
        return json.dumps(self.serialize())

