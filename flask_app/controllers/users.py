from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = {
        'firstname' : request.form['firstname'],
        'lastname' : request.form['lastname'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    print(data)
    if not User.validate_registration(request.form):
        return redirect('/')
    User.user_registration(data) # saving user to database
    flash('You have successfully registered!')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_user_by_email(request.form)
    if not user:
        flash('Email does not exists!')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password is incorrect!')
        return redirect('/')

    session['user_id'] = user.id
    session['email'] = user.email

    # print('Login works')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login first!")
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have successfully logged out!")
    return redirect('/')
