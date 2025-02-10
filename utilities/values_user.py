import sqlite3

conn = sqlite3.connect('data/biblioteca.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL,
    tipo INTEGER NOT NULL
)
''')

cursor.execute('''
INSERT INTO usuarios (nombre, correo, tipo)
VALUES (?, ?, ?)
''', ('Ezequiel', 'ezequiel@example.com', 'profesor'))

conn.commit()

cursor.execute('SELECT * FROM usuarios')
usuarios = cursor.fetchall()
print(usuarios)

conn.close()
