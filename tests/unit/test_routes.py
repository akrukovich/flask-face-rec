"""
This file (test_users.py) contains the functional tests for the users blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the users blueprint.
"""
from app.models import Face


def test_index(test_client):
    rv = test_client.get('/')
    assert rv.status_code == 200
    assert b'Home' in rv.data


def test_people_list(test_client, init_database):
    rv = test_client.get('/people_list')
    assert rv.status_code == 200
    assert b'Cristiano Ronaldo' in rv.data


def test_people_list_out_of_query(test_client, init_database):
    rv = test_client.get('/people_lists')
    assert rv.status_code == 404
    assert b'Not Found' in rv.data
    print(rv.data)


def test_add_face_correct_info(test_client, init_database):
    rv = test_client.post('/add_face', data=dict(
        name='Eminem',
        upload=open('tests/Eminem.jpeg', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 200
    assert b'Eminem' in rv.data
    assert Face.query.count() == 2


def test_add_face_repeated_info(test_client, init_database):

    rv = test_client.post('/add_face', data=dict(
        name='Ronaldo',
        upload=open('tests/Ronaldo.jpeg', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 200
    assert b'exists' in rv.data
    assert Face.query.count() == 1


def test_add_face_incorrect_name(test_client, init_database):

    rv = test_client.post('/add_face', data=dict(
        name='R',
        upload=open('tests/Ronaldo.jpeg', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 200
    assert b'Field must be between 2 and 50 characters long' in rv.data
    assert Face.query.count() == 1

    del rv

    rv = test_client.post('/add_face', data=dict(
        name='R'*55,
        upload=open('tests/Ronaldo.jpeg', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 200
    assert b'Field must be between 2 and 50 characters long' in rv.data
    assert Face.query.count() == 1


def test_add_face_incorrect_photo_format(test_client, init_database):

    rv = test_client.post('/add_face', data=dict(
        name='Messi',
        upload=open('tests/Messi.webp', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 200
    assert b'Images only!' in rv.data
    assert Face.query.count() == 1


def test_add_face_no_human_photo(test_client, init_database):

    rv = test_client.post('/add_face', data=dict(
        name='Shrek',
        upload=open('tests/Shrek.jpg', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 200
    assert b'This is not a human or bad image quality' in rv.data
    assert Face.query.count() == 1


def test_add_face_no_photo(test_client, init_database):

    rv = test_client.post('/add_face', data=dict(
        name='Eminem',
        upload=open('tests/Eminem_feat._Juice_WRLD_-_Godzilla_.mp3', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 200
    assert b'Images only!' in rv.data
    assert Face.query.count() == 1


def test_check_people_correct_data(test_client, init_database):
    rv = test_client.post('/check_people', data=dict(
        upload=open('tests/RonaldoMessi.jpg', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 200
    assert b'Ronaldo' in rv.data
    assert b'Unknown' in rv.data


def test_check_people_no_photo(test_client, init_database):

    rv = test_client.post('/check_people', data=dict(
        name='Eminem',
        upload=open('tests/Eminem_feat._Juice_WRLD_-_Godzilla_.mp3', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 200
    assert b'Images only!' in rv.data
    assert Face.query.count() == 1

def test_check_people_no_human_image(test_client, init_database):

    rv = test_client.post('/check_people', data=dict(
        name='Shrek',
        upload=open('tests/Shrek.jpg', 'rb')
    ), follow_redirects=True)

    assert rv.status_code == 200
    assert Face.query.count() == 1
    assert b'This is not a human or bad image quality' in rv.data
