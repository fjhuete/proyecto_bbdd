import funciones

db = funciones.conexionMDB("localhost","proyecto","usuario","proyecto")

funcion=funciones.menu()

while funcion != 7:
   
   if funcion == 1:
      funciones.listar(db)
      
      funcion=funciones.menu()