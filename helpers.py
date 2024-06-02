import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class GameForm(FlaskForm):
    name = StringField('Game Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    category = StringField('Category', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    save = SubmitField('Save')

class UserForm(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def retrieve_image(id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}' in filename:
            return filename

    return 'default_cover.jpg'

def delete_file(id):
    file = retrieve_image(id)
    if file != 'default_cover.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))
