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
    
    username = StringField('username',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"CoolUsername123"})
    email = StringField('Email',validators=[
        DataRequired(),Email()
        ], render_kw={"placeholder":"someone@domain.com"})
    password = PasswordField('Password',validators=[DataRequired()], render_kw={"placeholder":"******"})
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo(password)], render_kw={"placeholder":"******"})
    submit = SubmitField('Sign Up')

    def validacionEmail(self, email):
        validacionExtra(lambda x : not db.userExists(x.data), email.data, "Email no valido")

    

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()], render_kw={"placeholder":"someone@domain.com"})
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