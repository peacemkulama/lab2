from flask import Blueprint, jsonify
from pony.orm import *
from orm import Photo

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/api/json', methods=['GET'])
def api_json():
    # Establish a database session
    with db_session:
        # Fetch all photos from the database and order them by descending time
        photo_list = [p.to_dict() for p in Photo.select().order_by(desc(Photo.time))]

        # Return the photo list as JSON response
        return jsonify(photo_list)
