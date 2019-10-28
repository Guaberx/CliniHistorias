from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo, NumberRange
from app import db

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


#Empresa
class RegistrarUsuarioEmpresaForm(FlaskForm):
    tiposDocumentos = [('1', 'Cedula'), ('2', 'Pasaporte'), ('3', 'Cedula de Extranjeria')]
    tipoDocumento = SelectField('Tipo de Documento', choices=tiposDocumentos)
    numeroDocumento = StringField('Numero de Documento', validators=[DataRequired(), NumberRange(min=0,max=99999999999999999999)], render_kw={"placeholder":"Escriba el numero de documento..."})
    nombre = StringField('Nombre',validators=[DataRequired(),Length(min=2, max=50)], render_kw={"placeholder":"Pepito"})
    apellido = StringField('Apellido',validators=[DataRequired(),Length(min=2, max=50)], render_kw={"placeholder":"Perez"})
    submit = SubmitField('Login')

class SolicitarPruebasEmpresaForm(FlaskForm):
    numeroDocumento = StringField('Numero de Documento', validators=[DataRequired(), NumberRange(min=0,max=99999999999999999999)], render_kw={"placeholder":"Id Usuario"})
    __Examenes = ['Sangre', 'Tac', 'Orina']
    __Especialistas = ['Internista', 'Gastroenterologo', 'Ginecologo', 'Otorrinolaringologo', 'Oftalmologo', 'Fonoaudiologo', 'Oncologo']
    
    marcasExamenes = []
    for i in __Examenes:
        marcasExamenes.append(BooleanField(i))
    
    marcasEspecialistas = []
    for i in __Especialistas:
        marcasEspecialistas.append(BooleanField(i))
    
    submit = SubmitField('Login')

class SolicitarResultadosEmpresaForm(FlaskForm):
    numeroDocumento = StringField('Numero de Documento', validators=[DataRequired(), NumberRange(min=0,max=99999999999999999999)], render_kw={"placeholder":"Escriba el numero de documento..."})
    submit = SubmitField('Login')

#Admin
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
    nombre = StringField('Nombre Empresa',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Nombre de la Empresa"})
    submit = SubmitField('Crear Empresa')

class AgregarUsuarioMedico(FlaskForm):
    nombre = StringField('Nombre Medico',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Nombre"})
    apellido = StringField('Nombre Medico',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Apellido"})
    tiposDocumentos = [('Cedula', 'Cedula'), ('Tarjeta de Identidad', 'Tarjeta de Identidad'),('Pasaporte', 'Pasaporte'), ('Cedula de Extranjeria', 'Cedula de Extranjeria')]
    tipoDocumento = SelectField('Tipo de Documento', choices=tiposDocumentos)
    tiposMedicos = [('Cardiologo', 'Cardiologo'), ('Ortopedista','Ortopedista'), ('Enfermero','Enfermero'), ('Laboratorista','Laboratorista') ]
    tipoMedico = SelectField('Tipo de Documento', choices=tiposMedicos)
    numeroDocumento = StringField('Nombre Medico',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Numero Documento."})
    submit = SubmitField('Crear Medico')

class AgregarUsuarioRecepcionista(FlaskForm):
    nombre = StringField('Nombre Medico',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Nombre"})
    apellido = StringField('Nombre Medico',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Apellido"})
    tiposDocumentos = [('Cedula', 'Cedula'), ('Tarjeta de Identidad', 'Tarjeta de Identidad'),('Pasaporte', 'Pasaporte'), ('Cedula de Extranjeria', 'Cedula de Extranjeria')]
    tipoDocumento = SelectField('Tipo de Documento', choices=tiposDocumentos)
    numeroDocumento = StringField('Nombre Medico',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Numero Documento."})
    submit = SubmitField('Crear Medico')

class AgregarUsuarioPaciente(FlaskForm):
    nombre = StringField('Nombre Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Nombre"})
    apellido = StringField('Nombre Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Apellido"})
    tiposDocumentos = [('Cedula', 'Cedula'), ('Tarjeta de Identidad', 'Tarjeta de Identidad'),('Pasaporte', 'Pasaporte'), ('Cedula de Extranjeria', 'Cedula de Extranjeria')]
    tipoDocumento = SelectField('Tipo de Documento', choices=tiposDocumentos)
    numeroDocumento = StringField('Nombre Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Numero Documento."})
    submit = SubmitField('Crear Paciente')

class AgregarUsuarioAdmin(FlaskForm):
    nombre = StringField('Nombre Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Nombre"})
    apellido = StringField('Nombre Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Apellido"})
    tiposDocumentos = [('Cedula', 'Cedula'), ('Tarjeta de Identidad', 'Tarjeta de Identidad'),('Pasaporte', 'Pasaporte'), ('Cedula de Extranjeria', 'Cedula de Extranjeria')]
    tipoDocumento = SelectField('Tipo de Documento', choices=tiposDocumentos)
    numeroDocumento = StringField('Nombre Paciente',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"Numero Documento."})
    submit = SubmitField('Crear Admin')