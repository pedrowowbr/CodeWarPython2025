import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from code_war.app import app
from code_war.database import get_session
from code_war.models import Base, Filme
from code_war.schemas import FilmePublic


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def filme(session):
    filme = Filme(
        tmdb_id=999,
        titulo='Matrix',
        titulo_original='The Matrix',
        idioma_original='en',
        popularidade=123.4,
        media_votos=8.7,
        contagem_votos=25000,
        data_lancamento='1999-03-31',
        overview='Um hacker descobre a verdade sobre sua realidade.',
        caminho_poster='/matrix.jpg',
        generos='["Action", "Sci-Fi"]'  # ← Atualização aqui
    )
    session.add(filme)
    session.commit()
    session.refresh(filme)
    return FilmePublic.from_orm(filme).dict(by_alias=True)
