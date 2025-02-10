import sqlite3
import os

db_path = os.path.join('data', 'biblioteca.db')

if not os.path.exists(db_path):
    print(f"Error: La base de datos no se encuentra en la ruta {db_path}")
else:
    print(f"La base de datos se encuentra en: {db_path}")

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE libros SET estado = 'disponible' WHERE estado = 'prestados'")
        conn.commit()
        print("Todos los libros han sido actualizados a 'disponible'.")
    except sqlite3.Error as e:
        print(f"Ocurrió un error al intentar actualizar la base de datos: {e}")

    conn.close()
