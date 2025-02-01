import sqlite3

# Conectar con la base de datos (reemplaza con el nombre correcto)
conexion = sqlite3.connect('data/biblioteca.db')  
cursor = conexion.cursor()

# Ejecutar la consulta para actualizar los libros prestados a disponibles
cursor.execute("UPDATE biblioteca SET estado = 'disponible' WHERE estado = 'prestado'")
conexion.commit()

print("Todos los libros prestados han sido marcados como disponibles.")

# Cerrar la conexión
conexion.close()
