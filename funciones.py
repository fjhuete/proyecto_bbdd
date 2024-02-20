import sys, MySQLdb

def conexionMDB(host,usuario,contraseña,nombrebd):
    try:
        db = MySQLdb.connect(host,usuario,contraseña,nombrebd)

    except:
        print("No se ha podido realizar la conexión a la base de datos.")
        sys.exit(1)

    return db

def desconexion(db):
    db.close()


def menu():
   funcion=int(input('''
Menú
========================================================
1. Listar el código de versión y su fecha de liberación
2. Filtrar versiones liberadas por año
3. Buscar el programador responsable de una versión
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