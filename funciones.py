import sys, MySQLdb, psycopg2

def conexionMDB(host,usuario,contraseña,nombrebd):
    try:
        db = MySQLdb.connect(host,usuario,contraseña,nombrebd)

    except:
        print("No se ha podido realizar la conexión a la base de datos.")
        sys.exit(1)

    return db

def conexionPS(host,usuario,contraseña,nombrebd):
    try:
        db = psycopg2.connect(host=host,database=nombrebd,user=usuario,password=contraseña)
    except:
        print("No se ha podido realizar la conexión a la base de datos.")
        sys.exit(1)

    return db

def desconexion(db):
    db.close()


def menu():
   funcion=int(input('''
Menú
============================================================
1. Listar las versiones con su programador responsable
2. Filtrar los datos de cada versión filtrada por su código
3. Buscar las versiones lanzadas en un año
4. Insertar registro en la tabla probadores
5. Eliminar versiones anteriores a una fecha
6. Actualizar telófono de la tabla probadores
7. Salir
                     
'''))
   return funcion


#1. Listar el código de versión y la fecha de liberación de las versiones.
def listar(db):
    sql="select nombre,apellido1,apellido2,v.codigoversion from programadores p left join versiones v on p.dni = v.dni order by apellido1"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        datos = cursor.fetchall()
        print('''
Nombre  Apellidos               Versión
========================================''')
        for dato in datos:
            print(dato[0],"     ",dato[1],"     ",dato[2],"     ",dato[3])
    except:
        print("Error en la consulta")
    sql="select * from versiones"
    try:
        cursor.execute(sql)
        print('''
En total hay %d versiones registradas'''%(cursor.rowcount))
    except:
        print("Error en la consulta")


#2. Indica una versión y muestra todas sus datos
def buscar(db):
    cod=input("Indica el código de la version que quieres consultar: ")
    sql="select fechaliberacion,fechacomienzo,nombre,apellido1,apellido2,p.dni from versiones v, programadores p where v.dni = p.dni and v.codigoversion = '%s'"%cod
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        datos = cursor.fetchall()
        print('''
Comienzo                Liberación              Nombre              Apellidos                     DNI
=============================================================================================================''')
        for dato in datos:
            print(dato[0],"     ",dato[1],"     ",dato[2],"     ",dato[3],"     ",dato[4],"     ",dato[5])
    except:
        print("Error en la consulta")