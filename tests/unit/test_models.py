""" Model tests."""
from face_recognition import load_image_file, face_encodings
import numpy as np


def test_new_person(new_person):

    image = load_image_file('tests/Ronaldo.jpeg')
    face_encoding = face_encodings(image)[0]

    face_encoding_str = face_encoding.tostring()
    face_encoding_np_array = np.fromstring(new_person.face_encodings)

    name = 'Cristiano Ronaldo'

    assert new_person.name == name
    assert new_person.__str__() == name
    assert face_encoding_str == new_person.face_encodings
    assert all([a == b for a, b in zip(face_encoding, face_encoding_np_array)])


