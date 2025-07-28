from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Float, Boolean
from code_war.database import Base


class Filme(Base):
    __tablename__ = 'filmes'
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    titulo_original = Column(String(200), nullable=False)
    idioma_original = Column(String(10), nullable=False)
    descricao = Column(String(1000), nullable=False)
    data_lancamento = Column(String(20), nullable=False)
    popularidade = Column(Float, nullable=False)
    media_votos = Column(Float, nullable=False)
    quantidade_votos = Column(Integer, nullable=False)
    poster = Column(String(300), nullable=True)
    backdrop = Column(String(300), nullable=True)
    adulto = Column(Boolean, nullable=False)
    generos = Column(String(300), nullable=True)

    data_inclusao = Column(DateTime, default=datetime.now(timezone.utc))
    data_edicao = Column(DateTime, nullable=True, default=None,
                         onupdate=datetime.now(timezone.utc))
    data_exclusao = Column(DateTime, nullable=True, default=None)
