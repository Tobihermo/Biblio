import sqlite3

conn = sqlite3.connect('data/biblioteca.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS reservas (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_libro INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    fecha_reserva TEXT NOT NULL,
    fecha_devolucion TEXT NOT NULL,
    FOREIGN KEY (id_libro) REFERENCES biblioteca(id_libro),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
)
''')

conn.commit()

conn.close()

print("Tabla 'reservas' creada exitosamente.")
