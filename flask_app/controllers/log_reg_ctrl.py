from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from ..models.log_reg_mdl import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    info = User.get_all()
    return render_template('index.html', all_email = info)