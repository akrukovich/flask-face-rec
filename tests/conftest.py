import pytest
from app import create_app, db
import os
from app.models import Face
from face_recognition import load_image_file, face_encodings
from config import TestConfig


@pytest.fixture(scope='module')
def new_person():
    image = load_image_file('tests/Ronaldo.jpeg')
    face_encoding = face_encodings(image)[0]
    image_face_encoding_str = face_encoding.tostring()
    person = Face(name='Cristiano Ronaldo',
                  face_encodings=image_face_encoding_str
                  )

    return person


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='function')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    image = load_image_file('tests/Ronaldo.jpeg')
    face_encs = face_encodings(image)[0]
    image_face_encoding_str = face_encs.tostring()
    person = Face(name='Cristiano Ronaldo',
                  face_encodings=image_face_encoding_str)
    db.session.add(person)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()
