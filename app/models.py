"""
Models for project.

This module demonstrates relation between business entities and database.

"""
from app import db


class Face(db.Model):
    """
    Model of each face.

    This class is relation mapper of face object and database.

     Attributes:
         id (int): Unique id: Primary key.
         name (str): Full name of face owner.
         face_encodings (bytes): bytes str of face encodings.

    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    face_encodings = db.Column(db.LargeBinary)

    def __str__(self):
        """
        Magic __str__ method.

        Return name of model instance.
        Returns:
            self.name: str name of object.

        """
        return self.name
