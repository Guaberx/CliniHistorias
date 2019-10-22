from flask import render_template, jsonify, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, RegistrarUsuarioEmpresaForm
from app import app, db
from pprint import pprint
@app.route('/')
@app.route('/home')
def home():
    path = 'home.html'
    Usuarios = db.getAllUsers('posts')
    for i in Usuarios:
        pprint(i)
    return render_template(path,  Personas = Usuarios)

@app.route('/hello/<user>')
def hello_name(user):
    userType = 1
    if userType:
        return render_template('hello.html', name = user)
    else:
        return 'PUTAS HARRY... PUTAS!'

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





usrType = 'empresa'
@app.route('/registrar', methods=['GET','POST'])
def registrar():
    if usrType == 'empresa':
        form = RegistrarUsuarioEmpresaForm()
        if form.validate_on_submit():
            flash(f'Usuario con documento {form.tipoDocumento.data} registrado exitosamente!', 'success')
            result = request.form
            return redirect(url_for('home'))
        return render_template('empresa/registrar_usuario_empresa.html', tittle='Registrar Usuario', form=form)
    else:
        return 'ERROR'

@app.route('/solicitar', methods=['GET','POST'])
def solicitar():
    if usrType == 'empresa':
        form = RegistrarUsuarioEmpresaForm()
        if form.validate_on_submit():
            flash(f'Usuario con documento {form.tipoDocumento.data} registrado exitosamente!', 'success')
            result = request.form
            return redirect(url_for('home'))
        return render_template('empresa/solicitar_resultados_usuario_examen.html', tittle='Registrar Usuario', form=form)
    else:
        return 'ERROR'

@app.route('/ver', methods=['GET','POST'])
def ver():
    if usrType == 'empresa':
        form = RegistrarUsuarioEmpresaForm()
        if form.validate_on_submit():
            flash(f'Usuario con documento {form.tipoDocumento.data} registrado exitosamente!', 'success')
            result = request.form
            return redirect(url_for('home'))
        return render_template('empresa/registrar_usuario_empresa.html', tittle='Registrar Usuario', form=form)
    else:
        return 'ERROR'