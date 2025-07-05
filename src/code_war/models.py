from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from code_war.database import Base


class Filme(Base):
    __tablename__ = 'filmes'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    titulo_original = Column(String(100), nullable=False)
    titulo_romanizado = Column(String(100), nullable=False)
    descricao = Column(String(500), nullable=False)
    diretor = Column(String(100), nullable=False)
    produtor = Column(String(100), nullable=False)
    data_lancamento = Column(String(4), nullable=False)
    duracao_min = Column(String(10), nullable=False)
    pontuacao_rotten_tomatoes = Column(String(10), nullable=False)

    data_inclusao = Column(DateTime, default=datetime.now(timezone.utc))
    data_edicao = Column(
        DateTime,
        nullable=True,
        default=None,
        onupdate=datetime.now(timezone.utc),
    )
    data_exclusao = Column(DateTime, nullable=True, default=None)
