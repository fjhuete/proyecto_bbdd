import sys, MySQLdb, psycopg2
from datetime import datetime

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
        nombre=0
        apellidos=0
        for dato in datos:
            if nombre < len(dato[0]):
                nombre=len(dato[0])
            if apellidos < len(dato[1])+len(dato[2]):
                apellidos = len(dato[1])+len(dato[2])
        print('''
Nombre'''," "*(nombre-3),"Apellidos"," "*(apellidos-6),"Versión",'''
''',"="*(6+(nombre-3)+9+(apellidos-6)+7+1))
        for dato in datos:
            print(dato[0]," "*(nombre-len(dato[0])+3),dato[1],dato[2]," "*(apellidos-len(dato[1])-len(dato[2])+3),dato[3])
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
    sql="select fechaliberacion,fechacomienzo,nombre,apellido1,apellido2,p.dni from versiones v, programadores p where v.dni = p.dni and v.codigoversion = UPPER('%s')"%cod
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        datos = cursor.fetchall()
        if cursor.rowcount==0:
            print("No hay ninguna versión asociada a ese código.")
        else:
            comienzo=0
            liberacion=0
            nombre=0
            apellidos=0
            for dato in datos:
                if comienzo < len(str(dato[0])):
                    comienzo=len(str(dato[0]))
                if liberacion < (len(str(dato[1]))):
                    liberacion = (len(str(dato[1])))
                if nombre < len (dato[2]):
                    nombre = len(dato[2])
                if apellidos < len(dato[3])+len(dato[4]):
                    apellidos = len(dato[3])+len(dato[4])
            print('''
Comienzo'''," "*(comienzo-5),"Liberación"," "*(liberacion-7),"Nombre"," "*(nombre-3),"Apellidos"," "*(apellidos-6),'''DNI
''',"="*(8+(comienzo-5)+10+(liberacion-7)+6+(nombre-3)+9+(apellidos-6)+3+1+14))
            for dato in datos:
                print(str(dato[0])," "*(comienzo-len(str(dato[0]))+3),dato[1]," "*(liberacion-len(str(dato[1]))+3),dato[2]," "*(nombre-len(dato[2])+3),dato[3],dato[4]," "*(apellidos-len(dato[3])-len(dato[4])+3),dato[5])
    except:
        print("Error en la consulta")

#3. Busca las versiones lanzadas en un año
def programadores(db):
    año=input("Indica el año que quieres buscar: ")
    sql="select v.codigoversion,pr.nombre,pr.apellido1,pr.apellido2,pr.email,count(*) from versiones v, probadores pr, subsistemas s, usuarios u, perfiles pe where v.codigosubsistema = s.codigosubsistema and s.codigoperfil = pe.codigoperfil and pe.dni = u.dni and u.dni = pr.dni and extract(year from fechacomienzo) = %s group by codigoversion,nombre,apellido1,apellido2,email"%año
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        datos = cursor.fetchall()
        if cursor.rowcount==0:
            print("No hay versiones lanzadas en ese año.")
        else:
            version=0
            nombre=0
            apellidos=0
            email=0
            for dato in datos:
                if version < len(dato[0]):
                    version = len(dato[0])
                if nombre < len(dato[1]):
                    nombre = len(dato[1])
                if apellidos < len(dato[2])+len(dato[3]):
                    apellidos = len(dato[2])+len(dato[3])
                if email < len(dato[4]):
                    email = len(dato[4])
            print('''
Versión'''," "*(version-4),"Nombre"," "*(nombre-3),"Apellidos"," "*(apellidos-6),"Email"," "*(email-2),'''Cantidad
''',"="*(7+(version-4)+6+(nombre-3)+9+(apellidos-6)+5+(email-2)+8+8))
            for dato in datos:
                print(dato[0]," "*(version-len(dato[0])+3),dato[1]," "*(nombre-len(dato[1])+3),dato[2],dato[3]," "*(apellidos-len(dato[2])-len(dato[3])+3),dato[4]," "*(email-len(dato[4])+9),dato[5])
    except:
        print("Error en la consulta")
    
#4. Insertar información en la tabla probadores
def insertar(db,probador):
    cursor = db.cursor()
    sql="insert into probadores values ('%s', '%s', '%s', '%s', '%s', '%s')" % (probador["dni"],probador["nombre"],probador["apellido1"],probador["apellido2"],probador["telefono"],probador["correo"])
    try:
        cursor.execute(sql)
        db.commit()
        print("Los datos de %s %s %s se han añadido con éxito a la tabla probadores."%(probador["nombre"],probador["apellido1"],probador["apellido2"]))
    except:
        print("Error al insertar.")
        db.rollback()

#5. Eliminar las versiones que tengan una fecha de liberación anterior al 28/04/2021.
def borrarMDB(db,fecha):
    fecha_dt = datetime.strptime(fecha, '%d/%m/%Y')
    sql="delete from versiones where FechaLiberacion < '%s'"%fecha_dt
    cursor = db.cursor()
    borrar=input("¿Ralmente quieres borrar las versiones anteriores al %r? "%(fecha))
    if borrar == "Sí" or borrar == "sí" or borrar == "si" or borrar == "Si":
        try:
            cursor.execute(sql)
            db.commit()
            if cursor.rowcount==0:
                print("No hay versiones anteriores a esa fecha.")
            else:
                print("Se han borrado con éxito las versiones anteriores al %s"%(fecha))
        except:
            print("Error al borrar.")
            db.rollback()

def borrarPS(db,fecha):
    sql="delete from Versiones where FechaLiberacion < to_date('%s','DD/MM/YYYY')" % (fecha)
    cursor = db.cursor()
    borrar=input("¿Ralmente quieres borrar las versiones anteriores al %s? "%(fecha))
    if borrar == "Sí" or borrar == "sí" or borrar == "si" or borrar == "Si":
        try:
            cursor.execute(sql)
            db.commit()
            if cursor.rowcount==0:
                print("No hay versiones anteriores al %s."%(fecha))
            else:
                print("Se han borrado con éxito las versiones anteriores al %s"%(fecha))
        except:
            print("Error al borrar.")
            db.rollback()

#6. Actualizar el nuevo teléfono de Paloma Palacio Mansilla: 684846151
def actualizar(db,probador):
    sql="update probadores set telefono = '%s' where nombre = '%s' and apellido1 = '%s' and apellido2 = '%s'"%(probador["telefono"],probador["nombre"],probador["apellido1"],probador["apellido2"])
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print("Información actualizada.")
    except:
        print("Error al insertar.")
        db.rollback()