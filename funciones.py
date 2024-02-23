import sys, MySQLdb, psycopg2, oracledb
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

def conexionOracle(host,usuario,contraseña):
    try:
        oracledb.init_oracle_client() # <-- Thick mode
        db = oracledb.connect(user=usuario, password=contraseña, host=host)
    except:
        print("No se ha podido realizar la conexión a la base de datos.")
        sys.exit(1)

    return db

def desconexion(db):
    db.close()


def menu():
    while True:
        try:
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
            break
        except:
            print("Error. Por favor indica el número de la opción del menú que quieres ejecutar:")
    return funcion


#1. Listar el código de versión y la fecha de liberación de las versiones.
def listar(db):
    sql="select nombre,apellido1,apellido2,v.codigoversion from programadores p left join versiones v on p.dni = v.dni order by apellido1"
    cursor = db.cursor()
    cursor.execute(sql)
    datos = cursor.fetchall()
    print("+","-"*(8+10+15+8+2),"+")
    print("| {:<8} {:<10}{:<15} {:>8} |".format("Nombre","Apellidos","","Versión"))
    print("+","-"*(8+10+15+8+2),"+")
    for dato in datos:
        print("| {:<8} {:<10}{:<15} {:>8} |".format(dato[0],dato[1],dato[2],str(dato[3] or "")))
    print("+","-"*(8+10+15+8+2),"+")
    sql="select * from versiones"
    try:
        cursor.execute(sql)
        print('''
En total hay %d versiones registradas'''%(cursor.rowcount))
    except:
        print("Error en la consulta")

def listarOracle(db):
    sql="select nombre,apellido1,apellido2,v.codigoversion from programadores p left join versiones v on p.dni = v.dni order by apellido1"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        datos = cursor.fetchall()
        print("+","-"*(8+10+15+8+2),"+")
        print("| {:<8} {:<10}{:<15} {:>8} |".format("Nombre","Apellidos","","Versión"))
        print("+","-"*(8+10+15+8+2),"+")
        for dato in datos:
            print("| {:<8} {:<10}{:<15} {:>8} |".format(dato[0],dato[1],dato[2],str(dato[3] or "")))
        print("+","-"*(8+10+15+8+2),"+")
    except:
        print("Error en la consulta")
    sql="select * from versiones"
    try:
        cursor.execute(sql)
        print('''
En total hay %d versiones registradas'''%(len(cursor.fetchall())))
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
            print("+","-"*(22+22+10+10+15+10+4),"+")
            print("| {:<22} {:<22} {:<10} {:<10}{:<15} {:<10} |".format("Comienzo","Liberación","Nombre","Apellidos","","DNI"))
            print("+","-"*(22+22+10+10+15+10+4),"+")
            for dato in datos:
                print("| {:<22} {:<22} {:<10} {:<10}{:<15} {:<10} |".format(str(dato[0]),str(dato[1]),dato[2],dato[3],dato[4],dato[5]))
            print("+","-"*(22+22+10+10+15+10+4),"+")
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
            print("+","-"*(8+10+10+10+26+9+4),"+")
            print("| {:<8} {:<10} {:<10}{:<10} {:<26} {:>9} |".format("Versión","Nombre","Apellidos","","Email","Cantidad"))
            print("+","-"*(8+10+10+10+26+9+4),"+")
            print("\n".join("| {:<8} {:<10} {:<10}{:<10} {:<26} {:>9} |".format(*dato) for dato in datos))
            print("+","-"*(8+10+10+10+26+9+4),"+")
    except:
        print("Error en la consulta")
    
#4. Insertar información en la tabla probadores
def insertar(db,probador):
    cursor = db.cursor()
    sql="insert into probadores values ('%s', '%s', '%s', '%s', '%s', '%s')" % (probador["dni"],probador["nombre"],probador["apellido1"],probador["apellido2"],probador["telefono"],probador["correo"])
    try:
        cursor.execute(sql)
        db.commit()
        print('''Los datos de %s %s %s se han añadido con éxito a la tabla probadores.
Se ha añadido %d registro.'''%(probador["nombre"],probador["apellido1"],probador["apellido2"],cursor.rowcount))
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
                print('''Se han borrado con éxito las versiones anteriores al %s.
Se han boarrado %d registros.'''%(fecha,cursor.rowcount))
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
                print('''Se han borrado con éxito las versiones anteriores al %s.
Se han boarrado %d registros.'''%(fecha,cursor.rowcount))
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
        print('''Información actualizada.
Se ha actualizado %d registro.'''%(cursor.rowcount))
    except:
        print("Error al actualizar.")
        db.rollback()