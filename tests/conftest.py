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
        titulo='A Viagem de Chihiro',
        titulo_original='千と千尋の神隠し',
        titulo_romanizado='Sen to Chihiro no Kamikakushi',
        descricao=(
            'Durante a mudança da família para os subúrbios, uma garota '
            'aventureira entra em um mundo governado por deuses, bruxas e '
            'espíritos.'
        ),
        diretor='Hayao Miyazaki',
        produtor='Toshio Suzuki',
        data_lancamento='2001',
        duracao_min='125',
        pontuacao_rotten_tomatoes='97',
    )
    session.add(filme)
    session.commit()
    session.refresh(filme)
    # Retorne como dict serializável pelo schema Pydantic
    return FilmePublic.from_orm(filme).dict(by_alias=True)
