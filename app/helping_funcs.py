"""
Utilities functions.

This module provides auxiliaries functions for routes.
"""
import glob
import os
from datetime import datetime
from functools import update_wrapper, wraps

from app.models import Face

import face_recognition

from flask import make_response

import numpy as np


def get_known_face_encodings():
    """
    Return a list of face encodings and names of all entities.

    Function gets from db all str-typed encodings with relative names and
    convert encoding to numpy array.

    Returns:
        encodings: list of  tuples of face encodings and names.
    """
    encodings = []

    for face in Face.query.all():
        encodings.append((np.fromstring(face.face_encodings), face.name))

    return encodings


def del_tmp():
    """
    Delete all temporary images.

    This function remove all tmp images from tmp folder.

    Returns:None
    """
    files = glob.glob('app/static/img/tmp/*.jpg', recursive=True)

    for file in files:
        try:
            os.remove(file)
        except OSError as error:
            print('Error: %s : %s' % (file, error.strerror))


def is_existed(test_image):
    """
    Check whether uploaded face in database.

    This function gets face encodings from uploaded image.
    If face from image already exists then  function return True and name of
    person, otherwise returns False, empty name and face encoding for saving
    in database.

    Args:
        test_image: upload image.

    Returns:
        name: name of a face entity.
        face_encodings: face encodings of upload image.

    """
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image,
                                                     face_locations
                                                     )
    known_face_encodings = get_known_face_encodings()

    for (_, _, _, _), face_encoding in zip(face_locations,
                                           face_encodings
                                           ):

        matches = get_matches(face_encoding, known_face_encodings)
        # If match
        name = get_name_from_matches(matches, known_face_encodings)

        if name != 'Unknown':
            return True, name, None

        return False, name, face_encodings[0]


def nocache(view):
    """
    Clear cache function.

    This function clear static cache before request of decorated
    route function.

    Args:
        view: route function.

    Returns:
         update_wrapper: clear-cached view.
    """

    @wraps(view)
    def no_cache(*args, **kwargs):

        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()

        response.headers['Cache-Control'] = 'no-store, no-cache, ' \
                                            'must-revalidate, post-check=0, ' \
                                            'pre-check=0, max-age=0'

        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'

        return response

    return update_wrapper(no_cache, view)


def load_image(image_data):
    """
    Return numpy array of loaded image.

    Args:
        image_data: image data from input.

    Returns:
        image_to_encode: image contents as numpy array.
    """
    image_to_encode = face_recognition.load_image_file(image_data)

    return image_to_encode


def get_matches(face_encoding, known_face_encodings):
    """
    Return matches of uploaded image and already existed.

    Each match is True value and oppositely mismatch is False.

    Args:
        face_encoding: np.array of face encoding.
        known_face_encodings: already existed encodings.

    Returns:
        matches: array of bool values.

    """
    matches = face_recognition.compare_faces(
        [encoding[0] for encoding in known_face_encodings],
        face_encoding
    )

    return matches


def get_name_from_matches(matches, known_face_encodings):
    """
    Return relative name to a match.

    if no match name = 'Unknown', otherwise name will be get from db.

    Args:
        matches:matches array.
        known_face_encodings:already existed encodings.

    Returns:
        name: name of the match.
    """
    name = 'Unknown'

    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_encodings[first_match_index][1]

    return name


def draw_image(name, draw, top, right, bottom, left):
    """
    Draw image with names frames.

    Args:
        name: name of person.
        draw: PIL.ImageDraw object.
        top: top face location.
        right: right face location.
        bottom: bottom face location.
        left: left face location.

    Returns: None.

    """
    draw.rectangle(
        ((left, top), (right, bottom)), outline=(255, 255, 0)
    )
    # Draw label
    text_width, text_height = draw.textsize(name)
    draw.rectangle(
        ((left, bottom - text_height - 10), (right, bottom)),
        fill=(255, 255, 0),
        outline=(255, 255, 0)
    )
    draw.text((left + 6, bottom - text_height - 5),
              name,
              fill=(0, 0, 0)
              )
