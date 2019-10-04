from flask import render_template, jsonify, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm
from app import app, db

@app.route('/')
@app.route('/home')
def home():
    path = 'home.html'
    Usuarios = db.getAllUsers()
    return render_template(path,  Personas = Usuarios)

@app.route('/hello/<user>')
def hello_name(user):
    return render_template('hello.html', name = user)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        result = request.form
        return "URRA!"
        return redirect(url_for('home'))
    return render_template('register.html', tittle='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Account Logged in for {form.email.data}!', 'success')
        result = request.form
        return redirect(url_for('home'))
    return render_template('login.html', tittle='Login', form=form)