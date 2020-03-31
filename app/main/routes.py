# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect, flash, request
import face_recognition
from PIL import Image, ImageDraw

from app import db
from app.models import Face
from app.main.forms import UploadForm, CheckImageForm
from app.nocache import nocache
from app.helping_funcs import del_tmp, get_known_face_encodings, is_existed
from app.main import bp


@bp.route('/')
@bp.route('/home')
def index():
    return render_template('index.html', title='Home-FaceID')


@bp.route('/add_face', methods=['POST', 'GET'])
def add_face():

    form = UploadForm()

    if form.validate_on_submit():
        try:
            loaded_image = face_recognition.load_image_file(form.upload.data)
            is_in, name, image_face_encoding = is_existed(loaded_image)

            if is_in:

                flash(f'This person already exists! ({name})')
                return redirect(url_for('index'))

            else:

                image_face_encoding_str = image_face_encoding.tostring()
                image = Face(name=form.name.data.title(), face_encodings=image_face_encoding_str)

                db.session.add(image)
                db.session.commit()

                flash(f'New person has been added! ({image.name})')

        except TypeError as e:

            flash('This is not a human or bad image quality')

        return redirect(url_for('main.index'))

    return render_template('add_image.html', form=form,title='Add Person')


@bp.route('/check_people', methods=['POST', 'GET'])
@nocache
def check_people():

    form = CheckImageForm()
    names = []
    title = 'Check people'

    if form.validate_on_submit():

        del_tmp()

        test_image = face_recognition.load_image_file(form.upload.data)
        # Find faces in test image
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image, face_locations)

        if not face_encodings:
            flash('This is not a human or bad image quality')
            return redirect(url_for('main.index'))

        pil_image = Image.fromarray(test_image)
        draw = ImageDraw.Draw(pil_image)

        known_face_encodings = get_known_face_encodings()

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            matches = face_recognition.compare_faces([encoding[0] for encoding in known_face_encodings], face_encoding,tolerance=0.6)
            name = "Unknown Person"
            # If match
            if any(matches):
                first_match_index = matches.index(True)
                name = known_face_encodings[first_match_index][1]
            # Draw box
            draw.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0))
            # Draw label
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(255, 255, 0),
                           outline=(255, 255, 0))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(0, 0, 0))

            names.append(name)

        del draw
        # Display image
        pil_image.save(f'app/static/img/tmp/tmp_image.jpg')

        return render_template('check_image.html', form=form, names=names,title=title)

    return render_template('check_image.html', form=form,title=title)

@bp.route('/people_list')
def people_list():

    page = request.args.get('page', 1, type=int)
    names = Face.query.paginate(page=page,per_page=5)

    return render_template('people_list.html', names=names,title='People List')
