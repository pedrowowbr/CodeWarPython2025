from http import HTTPStatus


def test_root_deve_retornar_ok(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'API de filmes do Studio Ghibli'}


def test_create_filme(client):
    response = client.post(
        '/filmes/',
        json={
            'titulo': 'Meu Amigo Totoro',
            'titulo_original': 'となりのトトロ',
            'titulo_romanizado': 'Tonari no Totoro',
            'descricao': 'Duas irmãs descobrem espíritos mágicos da floresta.',
            'diretor': 'Hayao Miyazaki',
            'produtor': 'Hayao Miyazaki',
            'data_lancamento': '1988',
            'duracao_min': '86',
            'pontuacao_rotten_tomatoes': '93',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['titulo'] == 'Meu Amigo Totoro'
    assert response.json()['diretor'] == 'Hayao Miyazaki'
    assert response.json()['id'] == 1


def test_read_filmes(client):
    response = client.get('/filmes/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json()['filmes'], list)


def test_update_filme(client, filme):
    response = client.put(
        f'/filmes/{filme["id"]}',
        json={
            'titulo': 'A Viagem de Chihiro - Editado',
            'titulo_original': '千と千尋の神隠し',
            'titulo_romanizado': 'Sen to Chihiro no Kamikakushi',
            'descricao': 'Editado',
            'diretor': 'Miyazaki',
            'produtor': 'Suzuki',
            'ano_lancamento': '2002',
            'duracao': '130',
            'pontuacao_rotten_tomatoes': '98',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['titulo'] == 'A Viagem de Chihiro - Editado'


def test_delete_filme(client, filme):
    response = client.delete(f'/filmes/{filme["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Filme excluído com sucesso'}
