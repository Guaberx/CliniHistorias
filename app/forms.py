from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo, NumberRange
from app import db
from app.constants import *

#Validaciones Extra
def validacionExtra(validacion, field, errmsg):
    if validacion(field):
        raise ValidationError(errmsg)

#Secret key in order to protect against modified cookies and crosside attacks

class RegistrationForm(FlaskForm):
    
    username = StringField('username',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"usuario123"})
    email = StringField('Email',validators=[
        DataRequired(),Email()
        ], render_kw={"placeholder":"someone@domain.com"})
    password = PasswordField('Password',validators=[DataRequired()], render_kw={"placeholder":"******"})
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo(password)], render_kw={"placeholder":"******"})
    submit = SubmitField('Sign Up')

    def validacionEmail(self, email):
        return not db.userExists(email)

    

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()], render_kw={"placeholder":"alguien@dominio.com"})
    password = PasswordField('Password',validators=[DataRequired()], render_kw={"placeholder":"******"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#Medico
class SiguientePacienteMedicoForm(FlaskForm):
    submit = SubmitField('Siguiente Paciente')
    
class EnviarExamenesMedicoForm(FlaskForm):
    tiposExamenes = []
    for i in EXAMENES:
        tiposExamenes.append((EXAMENES[i][0],EXAMENES[i][0]))
    examenes = SelectField('Examen a mandar', choices=tiposExamenes)
    dependencias = SelectMultipleField('Dependencias del examen', choices=tiposExamenes)
    submit = SubmitField('Mandar Examenes')

class LlenarHistoriaClinicaMedicoForm(FlaskForm):
    descripcion = StringField('Descripcion', validators=[DataRequired(), Length(min=0,max=99999999999999999999)], render_kw={"placeholder":"Escriba los sintomas"})
    resultados = StringField('Resultados',validators=[DataRequired(),Length(min=0, max=99999999999999999999)], render_kw={"placeholder":"Escriba los resultados del examen"})
    comentarios = StringField('Comentarios',validators=[DataRequired(),Length(min=0, max=99999999999999999999)], render_kw={"placeholder":"Escriba cosas a tener en cuenta (Este campo no debe contener informacion sensible o privada)"})
    submit = SubmitField('Guardar')

#Empresa
class MandarExamenEmpresaForm(FlaskForm):
    tiposMedicos = []
    for i in ESPECIALIDADES:
        tiposMedicos.append((ESPECIALIDADES[i],ESPECIALIDADES[i]))
    examenes = SelectField('Especialista', choices=tiposMedicos)
    date = DateField('Fecha de la Consulta')
    submit = SubmitField('Mandar Examenes')

class RegistrarUsuarioEmpresaForm(FlaskForm):
    email = StringField('Email',validators=[
        DataRequired(),Email()
        ], render_kw={"placeholder":"bananin@elpa.nadero"})
    password = PasswordField('Contraseña',validators=[DataRequired()], render_kw={"placeholder":"******"})
    nombre = StringField('Nombre Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Nombre"})
    apellido = StringField('Apellido Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Apellido"})
    tiposDocumentos = [('Cedula', 'Cedula'), ('Tarjeta de Identidad', 'Tarjeta de Identidad'),('Pasaporte', 'Pasaporte'), ('Cedula de Extranjeria', 'Cedula de Extranjeria')]
    tipoDocumento = SelectField('Tipo de Documento', choices=tiposDocumentos)
    numeroDocumento = StringField('Numero de Documento',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Numero Documento."})
    submit = SubmitField('Registrar Empleado')

#Recepcionista
class RecepcionistaAgregarAColaForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()], render_kw={"placeholder":"alguien@dominio.com"})
    submit = SubmitField('Agregar a Cola')

class RecepcionistaLlenarInscripcionForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()], render_kw={"placeholder":"alguien@dominio.com"})
    submit = SubmitField('Llenar Inscripcion')
#Admin
class EliminarUsuarioForm(FlaskForm):
    submit = SubmitField('Eliminar Usuario')

class AgregarUsuario(FlaskForm):
    tiposUsiario = [('Empresa', 'Empresa'), ('Medico', 'Medico'), ('Paciente', 'Paciente'), ('Recepcionista', 'Recepcionista'), ('Admin', 'Admin')]
    tipo = SelectField('Tipo de Usuario', choices=tiposUsiario)
    email = StringField('Email',validators=[
        DataRequired(),Email()
        ], render_kw={"placeholder":"bananin@elpa.nadero"})
    password = PasswordField('Contraseña',validators=[DataRequired()], render_kw={"placeholder":"******"})
    submit = SubmitField('Crear Usuario')

    # def validate_email(self, email):
    #     if db.userExists(email):
    #         raise ValidationError(f"El usuario {email} ya existe")

class AgregarUsuarioEmpresa(FlaskForm):
    nombre = StringField('Nombre de la Empresa',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Empresa S.A."})
    codigoIdentificacion = StringField('Codigo de Identificacion de la Empresa',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"AAA00BBB111"})
    submit = SubmitField('Crear Empresa')

class AgregarUsuarioMedico(FlaskForm):
    nombre = StringField('Nombre Medico',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Nombre"})
    apellido = StringField('Apellido Medico',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Apellido"})
    tiposDocumentos = [('Cedula', 'Cedula'), ('Tarjeta de Identidad', 'Tarjeta de Identidad'),('Pasaporte', 'Pasaporte'), ('Cedula de Extranjeria', 'Cedula de Extranjeria')]
    tipoDocumento = SelectField('Tipo de Documento', choices=tiposDocumentos)
    # tiposMedicos = [('Cardiologo', 'Cardiologo'), ('Ortopedista','Ortopedista'), ('Enfermero','Enfermero'), ('Laboratorista','Laboratorista') ]
    tiposMedicos = []
    for i in ESPECIALIDADES:
        tiposMedicos.append((ESPECIALIDADES[i],ESPECIALIDADES[i]))
    tipoMedico = SelectField('Especialidad', choices=tiposMedicos)
    numeroDocumento = StringField('Numero de Documento',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Numero Documento."})
    submit = SubmitField('Crear Medico')

class AgregarUsuarioRecepcionista(FlaskForm):
    nombre = StringField('Nombre Recepcionista',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Nombre"})
    apellido = StringField('Nombre Recepcionista',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Apellido"})
    tiposDocumentos = [('Cedula', 'Cedula'), ('Tarjeta de Identidad', 'Tarjeta de Identidad'),('Pasaporte', 'Pasaporte'), ('Cedula de Extranjeria', 'Cedula de Extranjeria')]
    tipoDocumento = SelectField('Tipo de Documento', choices=tiposDocumentos)
    numeroDocumento = StringField('Numero de Documento',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Numero Documento."})
    submit = SubmitField('Crear Recepcionista')

class AgregarUsuarioPaciente(FlaskForm):
    nombre = StringField('Nombre Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Nombre"})
    apellido = StringField('Apellido Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Apellido"})
    tiposDocumentos = [('Cedula', 'Cedula'), ('Tarjeta de Identidad', 'Tarjeta de Identidad'),('Pasaporte', 'Pasaporte'), ('Cedula de Extranjeria', 'Cedula de Extranjeria')]
    tipoDocumento = SelectField('Tipo de Documento', choices=tiposDocumentos)
    numeroDocumento = StringField('Numero de Documento',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Numero Documento."})
    submit = SubmitField('Crear Paciente')

class AgregarUsuarioAdmin(FlaskForm):
    nombre = StringField('Nombre Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Nombre"})
    apellido = StringField('Apellido Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Apellido"})
    tiposDocumentos = [('Cedula', 'Cedula'), ('Tarjeta de Identidad', 'Tarjeta de Identidad'),('Pasaporte', 'Pasaporte'), ('Cedula de Extranjeria', 'Cedula de Extranjeria')]
    tipoDocumento = SelectField('Tipo de Documento', choices=tiposDocumentos)
    numeroDocumento = StringField('Numero de Documento',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Numero Documento."})
    submit = SubmitField('Crear Admin')