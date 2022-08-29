import os
from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail

def save_picture(form_picture):
    random_hex = token_hex(8)
    _,  f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex  + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Reset password request', 
        sender='my e-mail', 
        recipients=[user.email])
    msg.body = f'''Use this link to reset password: {url_for('users.reset_token',
        token=token, _external=True)}. ignore this if you dont wanna reset password'''
    mail.send(msg)
