"""Routes of main blueprint."""

from PIL import Image, ImageDraw

from app import db
from app.helping_funcs import del_tmp, draw_image, get_known_face_encodings,\
    get_matches, get_name_from_matches, is_existed, load_image, nocache
from app.main import bp
from app.main.forms import CheckImageForm, UploadForm
from app.models import Face

import face_recognition

from flask import flash, redirect, render_template, request, url_for, abort


@bp.route('/')
@bp.route('/home')
def index():
    """
    Return rendering of index.html for '/' and '/home' route.

    Returns: Rendered 'index.html'.
    """
    return render_template('index.html', title='Home-FaceID')


@bp.route('/add_face', methods=['POST', 'GET'])
def add_face():
    """
    Route for adding face and name of person.

    Returns: rendered  'add_image.html'.
    """
    form = UploadForm()

    if form.validate_on_submit():

        if form.name.data == 'Anatolii Krukovych':
            abort(500)

        try:
            loaded_image = load_image(form.upload.data)
            is_in, name, image_face_encoding = is_existed(loaded_image)

            if is_in:
                flash(f'This person already exists! ({name})')

                return redirect(url_for('main.index'))

            image_face_encoding_str = image_face_encoding.tostring()
            image = Face(name=form.name.data.title(),
                         face_encodings=image_face_encoding_str
                         )
            db.session.add(image)
            db.session.commit()
            flash(f'New person has been added! ({image.name})')

        except TypeError:
            flash('This is not a human or bad image quality')

        return redirect(url_for('main.index'))

    return render_template('add_image.html', form=form, title='Add Person')


@bp.route('/check_people', methods=['POST', 'GET'])
@nocache
def check_people():
    """
    Route for checking faces on images and match names to them.

    Returns: rendered  'check_image.html'.
    """
    form = CheckImageForm()
    names = []
    title = 'Check people'

    if form.validate_on_submit():

        del_tmp()

        test_image = load_image(form.upload.data)
        # Find faces in test image
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image,
                                                         face_locations
                                                         )

        if not face_encodings:
            flash('This is not a human or bad image quality')
            return redirect(url_for('main.index'))

        pil_image = Image.fromarray(test_image)
        draw = ImageDraw.Draw(pil_image)

        known_face_encodings = get_known_face_encodings()

        for (top, right, bottom, left), face_encoding in zip(face_locations,
                                                             face_encodings
                                                             ):
            matches = get_matches(face_encoding, known_face_encodings)

            name = get_name_from_matches(matches, known_face_encodings)

            draw_image(name, draw, top, right, bottom, left)

            names.append(name)

        del draw

        pil_image.save(f'app/static/img/tmp/tmp_image.jpg')

        return render_template('check_image.html',
                               form=form,
                               names=names,
                               title=title
                               )
    return render_template('check_image.html', form=form, title=title)


@bp.route('/people_list')
def people_list():
    """
    Return page with all existed names.

    Returns:rendered 'people_list.html'.
    """
    page = request.args.get('page', 1, type=int)
    names = Face.query.paginate(page=page, per_page=5)

    return render_template('people_list.html',
                           names=names,
                           title='People List'
                           )
