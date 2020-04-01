"""Forms for main routes."""
from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired, FileAllowed, FileField, FileRequired

from wtforms import StringField, SubmitField, validators


class UploadForm(FlaskForm):
    """Upload image form."""

    name = StringField('Name', validators=[DataRequired(),
                                           validators.Length(min=2, max=50)
                                           ])
    upload = FileField('image', validators=[
        FileRequired('File was empty!'),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Submit')


class CheckImageForm(FlaskForm):
    """Checking image upload form."""

    upload = FileField('image', validators=[
        FileRequired('File was empty!'),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Submit')
