from http import HTTPStatus


def test_root_deve_retornar_ok(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'API de filmes do TMDb'}


def test_create_filme(client):
    response = client.post(
        '/filmes/',
        json={
            'tmdb_id': 100,
            'titulo': 'Inception',
            'titulo_original': 'Inception',
            'idioma_original': 'en',
            'popularidade': 321.0,
            'media_votos': 8.8,
            'contagem_votos': 250000,
            'data_lancamento': '2010-07-16',
            'overview': 'Um ladrão invade sonhos para roubar segredos.',
            'caminho_poster': '/inception.jpg',
            'generos': ['Action', 'Adventure', 'Sci-Fi'],  # ← Atualização aqui
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['titulo'] == 'Inception'
    assert response.json()['tmdb_id'] == 100
    assert response.json()['id'] == 1
    

def test_read_filmes(client):
    response = client.get('/filmes/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json()['filmes'], list)


def test_update_filme(client, filme):
    response = client.put(
        f'/filmes/{filme["id"]}',
        json={
            'tmdb_id': 999,
            'titulo': 'Matrix Reloaded',
            'titulo_original': 'The Matrix Reloaded',
            'idioma_original': 'en',
            'popularidade': 200.0,
            'media_votos': 7.2,
            'contagem_votos': 150000,
            'data_lancamento': '2003-05-15',
            'overview': 'Continuação da saga Matrix.',
            'caminho_poster': '/matrix_reloaded.jpg',
            'generos': ['Action', 'Sci-Fi']  # ← Atualização aqui
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['titulo'] == 'Matrix Reloaded'


def test_delete_filme(client, filme):
    response = client.delete(f'/filmes/{filme["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Filme excluído com sucesso'}
