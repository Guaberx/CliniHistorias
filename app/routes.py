#from flask import render_template, jsonify, url_for, flash, redirect, request, make_response
from flask import *
from app.forms import * #RegistrationForm, LoginForm, RegistrarUsuarioEmpresaForm, AgregarUsuario,
from app import app, db, bcrypt, COOKIENAME, CREATEUSERCOOKIE#,userLogin
from pprint import pprint
# from flask_login import login_user, current_user, logout_user, UserMixin
import datetime
from bson.objectid import ObjectId

@app.route('/')
@app.route('/home')
def home():
    username = request.cookies.get(COOKIENAME)
    if username:# TODO: Mejorar esta verificacion para ver que la cookie sea correspondiente
        tmpUserAux = username.split()
        user = db.getUserInfoById(tmpUserAux[0], ObjectId(tmpUserAux[1]))
        
        realizadas, espera = list(), list()
        for i in user['consultas']:
            if i['estadoConsulta'] == 'Realizada': realizadas.append(i)
            elif i['estadoConsulta'] == 'Espera': espera.append(i)
        consultas = []
        
        if len(realizadas) > len(espera): i1, i2 = len(espera), len(realizadas)
        else: i2, i1 = len(espera), len(realizadas)
        
        for i in range(i1):
            consultas.append((realizadas[i], espera[i]))

        if len(realizadas) > len(espera):
            for i in range(i1,i2):
                consultas.append((realizadas[i], ''))
        else:
            for i in range(i1,i2):
                consultas.append(('', espera[i]))  
        
        if tmpUserAux[0] == 'pacientes':
            return render_template('paciente/main.html', user=user, email=tmpUserAux[2], consultas = consultas)
        return render_template('hello.html', name = f"{user['nombre']} {user['apellido']}" )
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if db.userExists(form.email.data) and bcrypt.check_password_hash(db.getUserPasswordByEmail(form.email.data), form.password.data):
            flash(f'El usuario {form.email.data} ha ingresado!', 'success')
            response = make_response(redirect(url_for('home')))
            userLoginInfo = db.getUserInfoByEmail('users',form.email.data)
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(minutes=2)
            response.set_cookie(COOKIENAME, f"{userLoginInfo['type']} {userLoginInfo['userId']} {form.email.data}")#, expires=expire_date)
            # login_user(userLogin.User(db.getUserIdByEmail(form.email.data)), remember=form.remember.data ) #db.getUserIdByEmail(form.email.data)
            return response #redirect(url_for('home'))
        else:
            flash(f'Usuario y contraseña Invalidos', 'danger')
        result = request.form
    return render_template('login.html', tittle='Login', form=form)

@app.route('/medicosTest')
def medicosTest():
    # user = db.getUserInfoById(tmpUserAux[0], ObjectId(tmpUserAux[1]))
    return render_template('medicos/main.html')#, user=user, email=tmpUserAux[2], consultas = consultas)

@app.route('/admin')
def adminModule():
    usuarios = db.getAllUsers('users')
    return render_template('admin/main.html', usuarios=usuarios)

@app.route('/admin/agregar', methods=['GET','POST'])
def adminModuleAdd():
    form = AgregarUsuario()
    if form.validate_on_submit():
            flash(f'El usuario aun no ha sido creado.\nContinua creandolo.', 'primary')
            response = make_response(redirect(url_for('adminModuleAdd2')))
            tipoUsuario = form.tipo.data
            email = form.email.data
            hashedPassword = bcrypt.generate_password_hash(form.password.data)
            response.set_cookie(CREATEUSERCOOKIE, f"{tipoUsuario} {email} {hashedPassword}")#, expires=expire_date)
            return response
    return render_template('admin/agregar.html', form=form)

@app.route('/admin/agregar2', methods=['GET','POST'])
def adminModuleAdd2():
    forms = {
        'Empresa':AgregarUsuarioEmpresa(),
        'Medico':AgregarUsuarioMedico(),
        'Recepcionista':AgregarUsuarioRecepcionista(),
        'Paciente':AgregarUsuarioPaciente(),
        'Admin':AgregarUsuarioAdmin()
    }
    createSesionCookie = request.cookies.get(CREATEUSERCOOKIE)

    tmpAux = createSesionCookie.split()
    tipoUsuario = tmpAux[0]
    email = tmpAux[1]
    hashedPassword = tmpAux[2]
    if forms.get(tipoUsuario):
        if forms[tipoUsuario].validate_on_submit():
            flash(f'Usuario Creado Exitosamente!', 'success')
            creationData = dict()
            creationData['nombre'] = forms[tipoUsuario].nombre.data
            if tipoUsuario != 'Empresa':
                creationData['apellido'] = forms[tipoUsuario].apellido.data
                creationData['tipoDocumento'] = forms[tipoUsuario].tipoDocumento.data
                creationData['numeroDocumento'] = forms[tipoUsuario].numeroDocumento.data
            if tipoUsuario == 'Medico':
                creationData['tipoDeMedico'] = forms[tipoUsuario].tipoMedico.data
            db.createUsers(email,hashedPassword,tipoUsuario,creationData)
            response = make_response(redirect(url_for('home')))
            response.set_cookie(COOKIENAME,"", expires=1)
            return response
        return render_template('admin/agregar2.html', form=forms[tipoUsuario])
    else:
        flash(f'Algo salio mal.', 'warning')
        return redirect(url_for('home'))


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