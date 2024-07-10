from flask import Blueprint, render_template
from orm import *

show_bp = Blueprint('show_bp', __name__)


@show_bp.route('/show', methods=['GET'])
def show():
    with db_session:
        # Retrieve all photos from the database and order them by descending time
        photo_list = [p.to_dict() for p in Photo.select().order_by(desc(Photo.time))]

    # Render the 'show.html' template and pass the photo list as a parameter
    return render_template('show.html', photo_list=photo_list)
