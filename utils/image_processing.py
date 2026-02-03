import os
from PIL import Image
from secrets import token_hex
from flask import current_app

def save_profile_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)

    # Resize image
    output_size = (800, 800)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # Save
    i.save(picture_path)

    return picture_fn
