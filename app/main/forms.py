# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from flask_wtf.file import FileField, FileAllowed, FileRequired, DataRequired


class UploadForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    upload = FileField('image', validators=[
        FileRequired('File was empty!'),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Submit')


class CheckImageForm(FlaskForm):

    upload = FileField('image', validators=[
        FileRequired('File was empty!'),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Submit')