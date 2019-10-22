from pymongo import MongoClient

#Esta coleccion contiene todo los datos de login de los usuarios y el tipo de usuario
users = [
    {
        'id':1, # id del objeto dentro de la coleccion users
        'tipo': 'empresas', #empresa, pacientes, admin, recepcionistas, medicos
        'userId': 5, # el id dentro de la coleccion a la que pertenece este usuario
        'correo':'bla@bla.com', # Correo para identificar al usuario al hacer login
        'contrasena': 'fasrgg64ggfgg34WGH%$' # La contraseña se guarda como un hash
    }
]

#Esta coleccion contiene la informacion de las empresas inscritas en el sistema
empresas = [
    {
        'id':5, # id del objeto dentro de la coleccion empresas
        'empleados':[2,3,4] # Una lista de de id de la coleccion pacientes de los empleados de esta empresa
    }
]

#Esta coleccion contiene toda la informacion de los pacientes inscritos en el sistema
pacientes = [
    {
        'id': 6, # id del objeto dentro de la coleccion pacientes.
        'tipoDocumento': 'cc', # tipo de documento. cedula, pasaporte, tarjeta de identidad, cedula de extranjeria.
        'numeroDocumento': 114451651, # numero del documento.
        'historiaClinica': {}, # Objeto que contiene toda la informacion de los campos relacionados con la historia clinica del paciente, que se llena al momento de inscripcion.
        'consultasRealizadas':[], # una lista de los id de las consultas realizadas. Es utilizada para ver si las dependencias de una consulta se han cumplido o no.
        'consultas':[ # Tanto un examen como una consulta se consideran consultas, es decir que se tratan los roles de la misma manera.
            {
                'idConsulta':5,
                'fecha':'11-00-02',
                'descripcion': 'Esta es la descripcion de de la consulta. ej: ep paciente presenta dolor de cabeza...',
                'resultados':'Estos son los resultados, incluyendo. ej: tiene un virus de inmuno deficiencia adquirida',
                'comentarios': 'Estos son los comentarios que pupede leer la empresa. ej: el paciente no debe estar expuesto a ambientes toxicos',
                'dependencias':[1,2,3,4], # una lista de los id de las consultas que tienen que realizarse para poder realizar esta consulta.
                'estadoConsulta': 'Espera', #Realizada, Espera, Activa.
                'atendio':[ # Informacion sobre quien hizo la consulta o examen.
                    {
                        'id':7,
                        'nombre': 'Pepe',
                        'apellido': 'perez',
                        'tipoMedico': 'Medico general'
                    }
                    ]
            }
        ]
    }
]

#Esta coleccion contiene la informacion de medicos, especialistas, laboratoristas y enfermeros.
medicos = [
    {
        'id':7,
        'nombre': 'Pepe',
        'apellido': 'perez',
        'tipoMedico': 'Medico general',
        'atenciones':[
            {
                'idPaciente':6,
                'idHistoriaPaciente': 5,

            }
        ]
    }
]

#Esta coleccion contiene la informacion de las recepcionistas
recepcionistas = [
    {
        'id':7,
        'nombre': 'Pepe',
        'apellido': 'perez',
    }
]

#Esta coleccion contiene la informacion de los administradores del sistema
admin = [
    {
        'id':7,
        'nombre': 'Pepe',
        'apellido': 'perez',
    }
]

#Esta coleccion se utliza para m
cola = {
    'enConsulta': ['idUsuario1'], # Guarda los usuarios que estan actualmente en alguna consulta, de esta manera, un usuario no sera llamado a otra consulta mientras este en una
    #El resto de listas en el objeto cola hace referencia a la cola de cada especialista. De esta manera cuando un cardiologo, por ejemplo, llame al siguiente en su cola. Se haran cambios solo sobre la cola correspondiente a los cardiologos. es decir, la cola esta ordenada para cada especialista
    'cardiologo': ['idUsuario1', 'idUsuario2'],
    'reumatologo': ['idUsuario2', 'idUsuario5']
}

class DB:
    
    def __init__(self, dbUrl):#'mongodb://localhost:27017'
        # self.client = MongoClient()
        self.__client = MongoClient(dbUrl)
        self.__db = self.__client['test']
        self.__acceptedRoles = ['empresas','pacientes','admin','medicos', 'recepcionistas']

    #CREATES
    def createUsers(self, email, hashedPassword, userType, creationData = {}):
        #Read others
        #Modify others
        #db.posts.update_one({'_id':x , 'Consultas.id':1} , {'$set':{'Consultas.$.start.Dependencias' : [1,2,3,5,8] }} )
        #coll.update({'ref': ref}, {'$push': {'tags': new_tag}})
        #db.posts.update_one({'_id':x , 'Consultas.id':1} , {'$push':{'Consultas.$.start.Dependencias' : 15 }} )
        if userType in self.__acceptedRoles:
            if userType == 'empresas':
                data = {
                    'nombre':creationData['nombre'],
                    'empleados':creationData['empeados']
                }
            elif userType == 'pacientes':
                data = {
                    'nombre':creationData['nombre'],
                    'apellido':creationData['apellido'],
                    'fechaNacimiento':creationData['fechaNacimiento'],
                    'formularioPaciente':{},#Es un diccionario con todos los campos respectivos del hc
                    'tipoDocumento': creationData['tipoDocumento'],
                    'numeroDocumento': creationData['numeroDocumento'],
                    'consultaActivas':[],
                    'consultasRealizadas':[],
                    'consultasEspera': [],
                    'consultas':[]
                }
            elif userType == 'medicos':
                data = {
                    'nombre': creationData['nombre'],
                    'apellido':creationData['apellido'],
                    'tipoDocumento': creationData['tipoDocumento'],
                    'numeroDocumento': creationData['numeroDocumento'],
                    'tipoDeMedico': creationData['tipoDeMedico'] #Que especialidad/funcion en le EPS
                }
            elif userType == 'recepcionista':
                data = {
                    'nombre': creationData['nombre'],
                    'apellido':creationData['apellido'],
                    'tipoDocumento': creationData['tipoDocumento'],
                    'numeroDocumento': creationData['numeroDocumento'],
                }
            elif userType == 'admin':
                data = {
                    'nombre': creationData['nombre'],
                    'apellido':creationData['apellido'],
                    'tipoDocumento': creationData['tipoDocumento'],
                    'numeroDocumento': creationData['numeroDocumento'],
                }

            #Falta verificar si el usuario no existe antes de creatlo

            self.__db[userType].insert_one(data)
            tmpUserId = self.__db[userType].find_one({ "tipoDocumento":creationData['tipoDocumento'], "numeroDocumento":creationData['numeroDocumento']})['_id']
            self.__db.users.insert({
                'email':email,
                'password': hashedPassword,
                'type': userType,
                'userId': tmpUserId,
            })
            return True
        return False
    
    #GETS
    def userExists(self, email):
        tmp = self.__db[users].find_one({'email':email})
        if tmp: return True
        return False
        
    def getAllUsers(self, grupo):
        users = []
        for user in self.__db[grupo].find({}):
            users.append(user)
        return users

    def getUserInfo(self, grupo, query):
        usuarios = []
        for user in self.__db[grupo].find(query): 
            usuarios.append(user)
        return usuarios
    
    def buscarConsultasPosiblesUsuario(self, userEmail):
        pass

    #SETS
    def setUserParameter(self, grupo, searchQuery, dataQuery, newData):
        self.__db[grupo].update_one(searchQuery , {'$set':{dataQuery : newData }} )
    
    def appendUserParameter(self, grupo, searchQuery, dataQuery, newData):
        self.__db[grupo].update_one(searchQuery , {'$push':{dataQuery : newData }} )

    #DELETE