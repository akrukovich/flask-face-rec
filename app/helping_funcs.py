# -*- coding: utf-8 -*-
import numpy as np
import os
import glob
import face_recognition

from app.models import Face


def get_known_face_encodings():

    encodings = []

    for face in Face.query.all():
        encodings.append((np.fromstring(face.face_encodings), face.name))

    return encodings


def del_tmp():

    files = glob.glob('app/static/img/tmp/*.jpg', recursive=True)

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def is_existed(test_image):
    # Find faces in test image
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    known_face_encodings = get_known_face_encodings()

    name = ''

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([encoding[0] for encoding in known_face_encodings], face_encoding)

        # If match
        if any(matches):
            first_match_index = matches.index(True)
            name = known_face_encodings[first_match_index][1]

            return True, name, None

        return False, name, face_encodings[0]
