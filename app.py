# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:42:51 2019
"""

from flask import Flask, render_template, request
from upload_bp import upload_bp
from show_bp import show_bp
from search_bp import search_bp
from api_bp import api_bp
from UseSqlite import InsertQuery, RiskQuery
from datetime import datetime
from PIL import Image
from orm import *
import os

app = Flask(__name__)

app.register_blueprint(upload_bp)
app.register_blueprint(show_bp)
app.register_blueprint(search_bp)
app.register_blueprint(api_bp)


def make_html_paragraph(record):
    picture_name = record.split(', ')[2]
    image_path = './static/figure/' + picture_name

    if not os.path.exists(image_path):
        return ""

    im = Image.open(image_path)

    # Convert the image to RGB mode if it's not already in RGB or grayscale
    if im.mode not in ('RGB', 'L'):
        im = im.convert('RGB')

    im.save(image_path, 'JPEG')

    paragraph = f"<img src='/static/figure/{picture_name}' width='300px'><br />"
    paragraph += f"Description: {record.split(', ')[0]}<br />"
    paragraph += f"Time: {record.split(', ')[1]}<br />"

    return paragraph


def get_database_photos():
    rq = RiskQuery('./static/RiskDB.db')
    rq.instructions("SELECT * FROM photo ORDER By time desc")
    rq.do()
    record = '<p>My past photo</p>'
    for r in rq.format_results().split('\n\n'):
        record += '%s' % (make_html_paragraph(r))
    return record + '</table>\n'


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        time_str = datetime.now().strftime('%Y%m%d%H%M%S')
        new_filename = time_str + '.jpg'
        uploaded_file.save('./static/upload/' + new_filename)
        time_info = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        description = request.form['description']
        path = './static/upload/' + new_filename
      
        add_photo(time_info, description, path, new_filename)
        return '<p>You have uploaded %s.<br/> <a href="/">Return</a>.' % (uploaded_file.filename)
    else:
        page = render_template('upload.html')
        page += get_database_photos()
        return page


if __name__ == '__main__':
    app.run(debug=True)
