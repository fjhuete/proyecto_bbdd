import funciones

db = funciones.conexionMDB("localhost","proyecto","usuario","proyecto")

funcion=funciones.menu()

while funcion != 7:
   
   if funcion == 1:
      funciones.listar(db)
      
      funcion=funciones.menu()

   elif funcion == 2:
      funciones.buscar(db)

      funcion=funciones.menu()
   
   elif funcion == 3:
      funciones.programadores(db)

      funcion=funciones.menu()

   elif funcion == 4:
      print("Indica los datos que quieres introducir en la tabla probadores:")
      dict={}
      dict["dni"]=input("DNI: ")
      dict["nombre"]=input("Nombre: ")
      dict["apellido1"]=input("Primer apellido: ")
      dict["apellido2"]=input("Segundo apellido: ")
      dict["telefono"]=input("Teléfono: ")
      dict["correo"]=input("Correo electrónico: ")
      funciones.insertar(db,dict)

      funcion = funciones.menu()

   elif funcion == 5:
      fecha=input("Indica la fecha a partir de la que quieres borrar los registros: ")
      funciones.borrarMDB(db,fecha)

      funcion = funciones.menu()

   elif funcion == 6:
      print("Indica los datos que quieres modificar en la tabla probadores:")
      dict={}
      dict["nombre"]=input("Nombre: ")
      dict["apellido1"]=input("Primer apellido: ")
      dict["apellido2"]=input("Segundo apellido: ")
      dict["telefono"]=input("Nuevo teléfono: ")
      funciones.actualizar(db,dict)

      funcion = funciones.menu()

funciones.desconexion(db)