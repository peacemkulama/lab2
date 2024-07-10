from flask import Blueprint, request
from pony.orm import *
from orm import Photo
from datetime import datetime

upload_bp = Blueprint('upload_bp', __name__)


@upload_bp.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file from the request
    uploaded_file = request.files['file']

    # Get the current time and format it as a string
    time_info = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get the description from the request form
    description = request.form['description']

    # Save the uploaded file and get the path
    path = save_uploaded_file(uploaded_file)

    with db_session:
        # Create a new Photo object and store it in the database
        Photo(
            time=time_info,
            description=description,
            path=path,
            name=uploaded_file.filename
        )

    return '<p>You have uploaded %s.<br/> <a href="/">Return</a>.' % uploaded_file.filename


def save_uploaded_file(file):
    time_str = datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = time_str + '.jpg'
    path = './static/upload/' + new_filename

    # Save the image to the upload folder
    file.save(path)

    return path


