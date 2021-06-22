from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from ..models.log_reg_mdl import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign_up',methods =['POST'])
def sign_up():
    if not User.validate_signup(request.form):
        return redirect('/')
    
    hash_me = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'birthdate': request.form['birthdate'],
        'password': hash_me
    }
    user_id = User.create(data)
    session['client'] = user_id
    
    return redirect('/success/signup')

    
@app.route('/login',methods =['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    
    user = User.get_by_email({ "email": request.form['email']})
    session['client'] = user.id

    return redirect('success/login')
    
    
@app.route('/success/signup')
def reg_success():
    if 'client' not in session:
        return redirect('/')
    return render_template('success_reg.html', user = User.get_by_id({"id": session['client']}))


@app.route('/success/login')
def log_success():
    return render_template('success_log.html', user = User.get_by_id({"id": session['client']}))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

