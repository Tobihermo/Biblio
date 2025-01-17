import sqlite3

# Conexión a la base de datos (se crea si no existe)
conn = sqlite3.connect('data/biblioteca.db')
cursor = conn.cursor()

# Crear la tabla usuarios (si no existe ya)
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL,
    nivel_acceso INTEGER NOT NULL
)
''')

# Insertar datos en la tabla usuarios
cursor.execute('''
INSERT INTO usuarios (nombre, correo, nivel_acceso)
VALUES (?, ?, ?)
''', ('Juan Perez', 'juan.perez@example.com', 1))

# Confirmar los cambios
conn.commit()

# Mostrar los datos insertados
cursor.execute('SELECT * FROM usuarios')
usuarios = cursor.fetchall()
print(usuarios)

# Cerrar la conexión
conn.close()
