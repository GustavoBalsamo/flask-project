from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Users
from helpers import UserForm
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    next_page = request.args.get('next')
    form = UserForm()
    return render_template('login.html', next_page=next_page, form=form)

@app.route('/authenticate', methods=['POST',])
def authenticate():
    form = UserForm(request.form)
    user = Users.query.filter_by(nickname=form.nickname.data).first()
    password = check_password_hash(user.password, form.password.data)
    if user and password:
        session['logged_in_user'] = user.nickname
        flash(user.nickname + ' logged in successfully!')
        next_page = request.form['next']
        return redirect(next_page)
    else:
        flash('User not logged in.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['logged_in_user'] = None
    flash('Successfully logged out!')
    return redirect(url_for('index'))
