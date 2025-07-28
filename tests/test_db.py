from sqlalchemy import select
from code_war.models import Filme


def test_create_filme(session):
    filme = Filme(
        tmdb_id=123,
        titulo='Interstellar',
        titulo_original='Interstellar',
        idioma_original='en',
        popularidade=543.2,
        media_votos=8.6,
        contagem_votos=120000,
        data_lancamento='2014-11-07',
        overview='Uma jornada para salvar a humanidade através do espaço.',
        caminho_poster='/interstellar.jpg',
        generos='["Adventure", "Drama", "Sci-Fi"]'  # ← Atualização aqui
    )
    session.add(filme)
    session.commit()

    result = session.scalar(select(Filme).where(
        Filme.titulo == 'Interstellar'))
    assert result.tmdb_id == 123
    assert result.media_votos > 8
