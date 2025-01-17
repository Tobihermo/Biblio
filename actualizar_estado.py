import sqlite3
import os

# Define la ruta a la base de datos dentro de la carpeta 'data'
db_path = os.path.join('data', 'biblioteca.db')

# Verificar si la base de datos existe
if not os.path.exists(db_path):
    print(f"Error: La base de datos no se encuentra en la ruta {db_path}")
else:
    print(f"La base de datos se encuentra en: {db_path}")

    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)

    # Crear un cursor
    cursor = conn.cursor()

    # Intentar actualizar todos los libros que tienen el estado 'prestados' a 'disponible'
    try:
        cursor.execute(
            "UPDATE libros SET estado = 'disponible' WHERE estado = 'prestados'")
        conn.commit()
        print("Todos los libros han sido actualizados a 'disponible'.")
    except sqlite3.Error as e:
        print(f"Ocurrió un error al intentar actualizar la base de datos: {e}")

    # Cerrar la conexión
    conn.close()
