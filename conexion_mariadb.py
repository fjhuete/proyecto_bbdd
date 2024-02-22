import funciones

db = funciones.conexionMDB("localhost","proyecto","usuario","proyecto")

funcion=funciones.menu()

while funcion != 7:
   
   if funcion == 1:
      funciones.listar(db)
      
      funcion=funciones.menu()

   if funcion == 2:
      funciones.buscar(db)

      funcion=funciones.menu()
   
   if funcion == 3:
      funciones.programadores(db)

      funcion=funciones.menu()

   if funcion == 4:
      funciones.actualizar(db)

      funcion=funciones.menu()