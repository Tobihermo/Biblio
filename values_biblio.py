import sqlite3

# Conexión a la base de datos (se crea si no existe)
conn = sqlite3.connect('data/biblioteca.db')
cursor = conn.cursor()

# Crear la tabla biblioteca (si no existe ya)
cursor.execute('''
CREATE TABLE IF NOT EXISTS biblioteca (
    id_libro INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    autor TEXT NOT NULL,
    categoria TEXT NOT NULL,
    estado TEXT NOT NULL,
    id_estanteria INTEGER NOT NULL,
    id_estante INTEGER NOT NULL,
    nivel_acceso INTEGER NOT NULL 
)
''')

# Función para agregar un libro
def agregar_libro():
    print("Ingrese los detalles del libro:")
    nombre = input("Nombre del libro: ")
    autor = input("Autor del libro: ")
    categoria = input("Categoría del libro: ")
    estado = "disponible"  # El estado se establece como 'Disponible' por defecto
    id_estanteria = int(input("ID de la estantería: "))
    id_estante = int(input("ID del estante: "))
    id_acceso = int(input("Nivel de acceso necesario: "))
    
    # Insertar el libro en la tabla biblioteca
    cursor.execute('''
    INSERT INTO biblioteca (nombre, autor, categoria, estado, id_estanteria, id_estante, nivel_acceso)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, autor, categoria, estado, id_estanteria, id_estante, id_acceso))

    # Confirmar los cambios
    conn.commit()
    print("Libro agregado exitosamente.")

# Función para agregar múltiples libros
def agregar_varios_libros(cantidad):
    for i in range(cantidad):
        print(f"\nAgregando libro {i+1} de {cantidad}...")
        agregar_libro()

# Preguntar cuántos libros desea agregar
cantidad_libros = int(input("¿Cuántos libros desea agregar? "))
agregar_varios_libros(cantidad_libros)

# Consultar los libros agregados
cursor.execute('SELECT * FROM biblioteca')
biblioteca = cursor.fetchall()
print("\nLista de libros en la biblioteca:")
for libro in biblioteca:
    print(libro)

# Cerrar la conexión
conn.close()
