from flask import Blueprint, jsonify, render_template
from orm import *

search_bp = Blueprint('search_bp', __name__)


@search_bp.route('/search/<query_string>', methods=['GET'])
def search(query_string):
    with db_session:

        # Perform a database query to retrieve photos matching the provided query string
        photo_list = list(filter(lambda p: query_string in p['description'], get_photos()))
        print("Photo list", photo_list)

        photos = []
        for photo in photo_list:
            photo_data = {
                'description': photo['description'],
                'path': '/' + photo['path'][2:],
            }
            photos.append(photo_data)
        return render_template('photo_search_result.html', photo_list=photos)
