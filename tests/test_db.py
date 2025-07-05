from sqlalchemy import select

from code_war.models import Filme


def test_create_filme(session):
    filme = Filme(
        titulo='Meu Vizinho Totoro',
        titulo_original='となりのトトロ',
        titulo_romanizado='Tonari no Totoro',
        descricao='Espíritos mágicos da floresta.',
        diretor='Hayao Miyazaki',
        produtor='Hayao Miyazaki',
        data_lancamento='1988',
        duracao_min='86',
        pontuacao_rotten_tomatoes='93',
    )
    session.add(filme)
    session.commit()

    result = session.scalar(
        select(Filme).where(Filme.titulo == 'Meu Vizinho Totoro')
    )
    assert result.diretor == 'Hayao Miyazaki'
