import sqlite3

conexion = sqlite3.connect('data/biblioteca.db')  
cursor = conexion.cursor()

cursor.execute("UPDATE biblioteca SET estado = 'disponible' WHERE estado = 'prestado'")
conexion.commit()

print("Todos los libros prestados han sido marcados como disponibles.")

conexion.close()
