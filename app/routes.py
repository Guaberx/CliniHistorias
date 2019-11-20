from flask import *
from app.constants import *
from app.forms import * #RegistrationForm, LoginForm, RegistrarUsuarioEmpresaForm, AgregarUsuario,
from app import app, db, bcrypt#,userLogin
from pprint import pprint
import datetime
from bson.objectid import ObjectId

def checkSessionCookie():
    tmpSessionCookie = request.cookies.get(SESSIONCOOKIE)
    if tmpSessionCookie:# TODO: Mejorar esta verificacion para ver que la cookie sea correspondiente
        tmpSessionCookie = tmpSessionCookie.split()
        sessionCookie = {}
        sessionCookie['userType'] = tmpSessionCookie[0]
        sessionCookie['id'] = tmpSessionCookie[1]
        sessionCookie['email'] = tmpSessionCookie[2]
        return sessionCookie
    return None

@app.route('/')
@app.route('/home')
def home():
    tmpSession = checkSessionCookie()
    if tmpSession:
        if tmpSession['userType'] == USERTYPES[0]: #Empresa
            return redirect(url_for('empresaModule'))
        elif tmpSession['userType'] == USERTYPES[1]: #Medico
            return redirect(url_for('medicoModule'))
        elif tmpSession['userType'] == USERTYPES[2]: #Recepcionista
            return redirect(url_for('recepcionModule'))
        elif tmpSession['userType'] == USERTYPES[3]: #Paciente
            return redirect(url_for('pacienteModule'))
        elif tmpSession['userType'] == USERTYPES[4]: #Admin
            return redirect(url_for('adminModule'))

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
            response.set_cookie(SESSIONCOOKIE, f"{userLoginInfo['type']} {userLoginInfo['userId']} {form.email.data}")#, expires=expire_date)
            # login_user(userLogin.User(db.getUserIdByEmail(form.email.data)), remember=form.remember.data ) #db.getUserIdByEmail(form.email.data)
            return response #redirect(url_for('home'))
        else:
            flash(f'Usuario y contraseña Invalidos', 'danger')
        result = request.form
    return render_template('login.html', tittle='Login', form=form)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    response.set_cookie(SESSIONCOOKIE, '', expires=0)
    response.set_cookie(MEDICOATENCIONPACIENTECOOKIE, '', expires=0)
    response.set_cookie(MEDICOATENCIONESTADOCOOKIE, '', expires=0)
    return response

@app.route('/recepcion', methods=['GET','POST'])
def recepcionModule():
    sessionCookie = checkSessionCookie()
    if sessionCookie and sessionCookie['userType'] == USERTYPES[2]:
        user = db.getUserInfoById(sessionCookie['userType'], ObjectId(sessionCookie['id']))
        formAgregarACola = RecepcionistaAgregarAColaForm()
        formLlenarInscripcion = RecepcionistaLlenarInscripcionForm()
        if formAgregarACola.validate_on_submit():
            if db.userExists(formAgregarACola.email.data):
                pacienteId = db.getUserIdByEmail(formAgregarACola.email.data)
                tmpUser = db.getUserInfoById('users',ObjectId(pacienteId))
                paciente = db.getUserInfoById('Paciente',ObjectId(tmpUser['userId']))
                #Revisar que consultas pueden ser realizadas y luego agregarlas a la cola
                for i in paciente['consultas']:
                    possible = True
                    if i['estadoConsulta'] == 'Espera':
                        for j in i['dependencias']:
                            if j in paciente['consultasEspera']:
                                possible = False
                    if possible == True:
                        if len(db.getUserInfo('cola',{'type':i['especialista']})) == 0:
                            db.debug.cola.insert({'type':i['especialista'], 'data':[]})
                        if not paciente['_id'] in db.getUserInfo('cola',{'type':i['especialista']})[0]['data']:
                            db.appendUserParameter('cola', {'type':i['especialista']},'data',paciente['_id'])
                            flash(f"Paciente {formAgregarACola.email.data} agregado a cola de {i['especialista']}.","info")
                        else:
                            flash(f"No se agrego a {formAgregarACola.email.data} a cola de {i['especialista']} porque ya se encuentra en ella.","danger")
            else:
                flash(f"El paciente {formAgregarACola.email.data} no existe.","warning")
                    

        return render_template('recepcion/main.html', user=user, formAgregarACola=formAgregarACola, formLlenarInscripcion=formLlenarInscripcion)
    return redirect(url_for('home'))

@app.route('/empresa')
def empresaModule():
    sessionCookie = checkSessionCookie()
    if sessionCookie and sessionCookie['userType'] == USERTYPES[0]:
        user = db.getUserInfoById(sessionCookie['userType'], ObjectId(sessionCookie['id']))
        empleados = db.getUserInfo('users', {"_id":{"$in":user['empleados']}})
        for i in range(len(empleados)):
            tmpEmpleado = db.getUserInfo('Paciente',{'_id':ObjectId(empleados[i]['userId'])})
            empleados[i].update(tmpEmpleado[0])
 
        
        return render_template('empresa/main.html', user=user, empleados=empleados)
    return redirect(url_for('home'))

@app.route('/empresa/empleado/<email>', methods=['GET','POST'])
def empresaModuleEmpleado(email):
    sessionCookie = checkSessionCookie()
    if sessionCookie and sessionCookie['userType'] == USERTYPES[0]:
        mandarExamenForm = MandarExamenEmpresaForm()
        user = db.getUserInfoById(sessionCookie['userType'], ObjectId(sessionCookie['id']))
        empleadoUser = db.getUserInfoByEmail('users',email)
        empleado = db.getUserInfo('Paciente',{'_id':empleadoUser['userId']})[0]
        empleado.update(empleadoUser)
        if mandarExamenForm.validate_on_submit():
            tmpN = len(empleado['consultas'])
            consulta = {
                'idConsulta':tmpN,
                'fecha':str(mandarExamenForm.date.data),
                'descripcion': mandarExamenForm.examenes.data,
                'resultados':'','comentarios': '',
                'dependencias':[],
                'estadoConsulta': 'Espera',
                'especialista':mandarExamenForm.examenes.data,
                'atendio':[]
                }
            db.appendUserParameter('Paciente',{'_id':empleadoUser['userId']},"consultas", consulta)
            flash(f'Consulta agregada exitosamente.', 'success')
        return render_template('empresa/empleado.html', user=user, empleado=empleado, form=mandarExamenForm)
    return redirect(url_for('home'))

@app.route('/empresa/registrarEmpleado', methods=['GET','POST'])
def empresaModuleRegistrarEmpleado():
    sessionCookie = checkSessionCookie()
    if sessionCookie and sessionCookie['userType'] == USERTYPES[0]:
        user = db.getUserInfoById(sessionCookie['userType'], ObjectId(sessionCookie['id']))
        form = RegistrarUsuarioEmpresaForm()
        if form.validate_on_submit():
                email = form.email.data
                hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                if db.userExists(email):
                    flash(f'El usuario {email} ya existe. Intente con otro email.', 'warning')
                    return redirect(url_for('empresaModuleRegistrarEmpleado'))
                flash(f'El usuario ha sido creado exitosamente.', 'success')
                creationData ={}
                creationData['nombre'] = form.nombre.data
                creationData['apellido'] = form.apellido.data
                creationData['tipoDocumento'] = form.tipoDocumento.data
                creationData['numeroDocumento'] = form.numeroDocumento.data
                tmpId = db.createUsers(email,hashedPassword,USERTYPES[3],creationData)
                db.appendUserParameter('Empresa',{"_id":ObjectId(user['_id'])},"empleados",tmpId[0])
                return redirect(url_for('empresaModule'))
        return render_template('empresa/registrarEmpleado.html', form=form, user=user)
    return redirect(url_for('home'))

@app.route('/medico', methods=['GET','POST'])
def medicoModule():
    sessionCookie = checkSessionCookie()
    if sessionCookie and sessionCookie['userType'] == USERTYPES[1]:
        siguientePacienteForm = SiguientePacienteMedicoForm()
        formResultados = LlenarHistoriaClinicaMedicoForm()
        formOtrosExamenes = EnviarExamenesMedicoForm()
        user = db.getUserInfoById(sessionCookie['userType'], ObjectId(sessionCookie['id']))
        atencion = False
        paciente = None
        if siguientePacienteForm.validate_on_submit():
            tmpColaMedico = db.getUserInfo('cola',{"type":user['tipoDeMedico']})
            tmpColaOcupados = db.getUserInfo('cola',{"type":'enConsulta'})
            if len(tmpColaMedico) > 0 and len(tmpColaMedico[0]['data']) > 0:
                i = 0
                while tmpColaMedico[0]['data'][i] in tmpColaOcupados[0]['data']:
                    i+=1
                if i < len(tmpColaMedico[0]['data']):
                    pacienteId = tmpColaMedico[0]['data'][i]
                    #Agregamos a la cola de ocupados al paciente que es llamado
                    db.appendUserParameter('cola',{'type':'enConsulta'},'data',pacienteId)
                    return redirect(url_for('medicoModule2',pacienteId=pacienteId))
            else:
                flash(f"Aun no hay pacientes en la cola de {user['tipoDeMedico']}","danger")
        return render_template('medicos/main.html', user=user, paciente=paciente, atencion=atencion, siguientePacienteForm=siguientePacienteForm, formResultados=formResultados, formOtrosExamenes=formOtrosExamenes)
        
    return redirect(url_for('home'))


@app.route('/medico/<pacienteId>', methods=['GET','POST'])
def medicoModule2(pacienteId):
    sessionCookie = checkSessionCookie()
    if sessionCookie and sessionCookie['userType'] == USERTYPES[1]:
        siguientePacienteForm = SiguientePacienteMedicoForm()
        formResultados = LlenarHistoriaClinicaMedicoForm()
        formOtrosExamenes = EnviarExamenesMedicoForm()
        user = db.getUserInfoById(sessionCookie['userType'], ObjectId(sessionCookie['id']))
        atencion = True
        paciente = db.getUserInfoById('Paciente',ObjectId(pacienteId))
        
        if formResultados.validate_on_submit():
            flash(f'Consulta Terminada.', 'success')
            return redirect(url_for('medicoModule'))

        if formOtrosExamenes.validate_on_submit() and formOtrosExamenes.examenes.data != None:
            flash(f'Examanes agregados.', 'success')        
        
        return render_template('medicos/main.html', user=user, paciente=paciente, atencion=atencion, siguientePacienteForm=siguientePacienteForm, formResultados=formResultados, formOtrosExamenes=formOtrosExamenes)
        
    return redirect(url_for('home'))



@app.route('/paciente')
def pacienteModule():
    sessionCookie = checkSessionCookie()
    if sessionCookie and sessionCookie['userType'] == USERTYPES[3]:
        user = db.getUserInfoById(sessionCookie['userType'], ObjectId(sessionCookie['id']))
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

        return render_template('paciente/main.html', user=user, email=sessionCookie['email'], consultas = consultas, realizadas = realizadas, espera = espera)
    return redirect(url_for('home'))

@app.route('/admin')
def adminModule():
    usuarios = db.getAllUsers('users')
    eliminarUsuarioForm = EliminarUsuarioForm()
    return render_template('admin/main.html', usuarios=usuarios, eliminarUsuarioForm=eliminarUsuarioForm)

@app.route('/admin/eliminar/<email>')
def adminModuleDelete(email):
    user = db.getUserInfoByEmail('users',email)
    userId2 = user['userId']
    db.debug.users.delete_one({'_id':ObjectId(user['_id'])})
    db.debug[user['type']].delete_one({'_id':ObjectId(userId2)})
    return redirect(url_for('adminModule'))

@app.route('/admin/agregar', methods=['GET','POST'])
def adminModuleAdd():
    sessionCookie = request.cookies.get(SESSIONCOOKIE)
    form = AgregarUsuario()
    if form.validate_on_submit():
            response = make_response(redirect(url_for('adminModuleAdd2')))
            tipoUsuario = form.tipo.data
            email = form.email.data
            hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            response.set_cookie(CREATEUSERCOOKIE, f"{tipoUsuario} {email} {hashedPassword}")#, expires=expire_date)
            if db.userExists(email):
                flash(f'El usuario {email} ya existe. Intente con otro email.', 'warning')
                return redirect(url_for('adminModuleAdd'))
            flash(f'El usuario aun no ha sido creado.\nContinua creandolo.', 'primary')
            return response
    return render_template('admin/agregar.html', form=form)

@app.route('/admin/agregar2', methods=['GET','POST'])
def adminModuleAdd2():
    sessionCookie = request.cookies.get(SESSIONCOOKIE)
    forms = {
        USERTYPES[0]:AgregarUsuarioEmpresa(),
        USERTYPES[1]:AgregarUsuarioMedico(),
        USERTYPES[2]:AgregarUsuarioRecepcionista(),
        USERTYPES[3]:AgregarUsuarioPaciente(),
        USERTYPES[4]:AgregarUsuarioAdmin()
    }
    createUserCookie = request.cookies.get(CREATEUSERCOOKIE)
    response = make_response(redirect(url_for('home')))
    response.set_cookie(CREATEUSERCOOKIE, '', expires=0)

    tmpAux = createUserCookie.split()
    userType = tmpAux[0]
    email = tmpAux[1]
    hashedPassword = tmpAux[2]
    if forms.get(userType):
        if forms[userType].validate_on_submit():
            flash(f'Usuario Creado Exitosamente!', 'success')
            creationData = dict()
            creationData['nombre'] = forms[userType].nombre.data
            if userType != 'Empresa':
                creationData['apellido'] = forms[userType].apellido.data
                creationData['tipoDocumento'] = forms[userType].tipoDocumento.data
                creationData['numeroDocumento'] = forms[userType].numeroDocumento.data
            if userType == 'Medico':
                creationData['tipoDeMedico'] = forms[userType].tipoMedico.data
            db.createUsers(email,hashedPassword,userType,creationData)
            response = make_response(redirect(url_for('home')))
            response.set_cookie(SESSIONCOOKIE,"", expires=1)
            return response
        return render_template('admin/agregar2.html', form=forms[userType], userType=userType, usertypes=USERTYPES)
    else:
        flash(f'Algo salio mal.', 'warning')
        return redirect(url_for('home'))

#DEBUG THINGS. DONT LOOK AT THE CODE BELOW THIS LINE



# db.appendUserParameter('Paciente',{"nombre":"Pepito"},"consultas",{'idConsulta':5,'fecha':'11-00-02','descripcion': 'Esta es la descripcion de de la consulta. ej: ep paciente presenta dolor de cabeza...','resultados':'Estos son los resultados, incluyendo. ej: tiene un virus de inmuno deficiencia adquirida','comentarios': 'Estos son los comentarios que pupede leer la empresa. ej: el paciente no debe estar expuesto a ambientes toxicos','dependencias':[1,2,3,4],'estadoConsulta': 'Espera', 'atendio':[{'id':7,'nombre': 'Pepe','apellido': 'perez','tipoMedico': 'Medico general'}]})

# db.appendUserParameter('Paciente',{"nombre":"Pepito"},"consultas",{'idConsulta':5,'fecha':'11-00-02','descripcion': 'Esta es la descripcion de de la consulta. ej: ep paciente presenta dolor de cabeza...','resultados':'Estos son los resultados, incluyendo. ej: tiene un virus de inmuno deficiencia adquirida','comentarios': 'Estos son los comentarios que pupede leer la empresa. ej: el paciente no debe estar expuesto a ambientes toxicos','dependencias':[],'estadoConsulta': 'Espera', 'atendio':[{'id':7,'nombre': 'Pepe','apellido': 'perez','tipoMedico': 'Medico general'}]})




from flask import jsonify
from bson.json_util import dumps
from json import loads
@app.route('/dbdebug/<coleccion>')
def dbdebug(coleccion):
    return jsonify(loads(dumps(db.getAllUsers(coleccion))))

@app.route('/dbdebugquery/<coleccion>/<query1>/<query2>')
def dbdebugquery(coleccion,query1,query2):
    ans = db.debug.coleccion.find(query,query2)
    ans = jsonify(loads(dumps(ans)))
    return ans

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



