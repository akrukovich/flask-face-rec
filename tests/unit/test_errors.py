"""Errors tests module"""


def test_not_found_error(test_client):
    rv = test_client.get('/sadasd')

    assert rv.status_code == 404
    assert b'404 Not Found' in rv.data


def test_500(test_client):

    rv = test_client.post('/add_face', data=dict(
        name='Anatolii Krukovych',
        upload=open('tests/Shrek.jpg', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 500
    assert b'500' in rv.data