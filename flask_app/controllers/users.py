from flask_app import app
from flask import render_template, redirect, request, session
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
    # user = User.user_registration(data)
    return redirect('/')
