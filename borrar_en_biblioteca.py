import sqlite3

# Conexión a la base de datos (se crea si no existe)
conn = sqlite3.connect('data/biblioteca.db')
cursor = conn.cursor()

# Función para borrar un libro
def borrar_libro():
    print("Ingrese el ID del libro que desea borrar:")
    id_libro = int(input("ID del libro: "))
    
    # Verificar si el libro existe
    cursor.execute('SELECT * FROM biblioteca WHERE id_libro = ?', (id_libro,))
    libro = cursor.fetchone()
    
    if libro:
        # Confirmar antes de borrar
        print(f"\nLibro encontrado: {libro}")
        confirmacion = input("¿Está seguro de que desea borrar este libro? (s/n): ")
        
        if confirmacion.lower() == 's':
            # Borrar el libro de la tabla
            cursor.execute('DELETE FROM biblioteca WHERE id_libro = ?', (id_libro,))
            conn.commit()
            print("Libro borrado exitosamente.")
        else:
            print("Operación cancelada.")
    else:
        print("No se encontró un libro con ese ID.")

# Función para borrar varios libros
def borrar_varios_libros(cantidad):
    for i in range(cantidad):
        print(f"\nBorrando libro {i+1} de {cantidad}...")
        borrar_libro()

# Preguntar cuántos libros desea borrar
cantidad_libros = int(input("¿Cuántos libros desea borrar? "))
borrar_varios_libros(cantidad_libros)

# Consultar los libros restantes en la tabla
cursor.execute('SELECT * FROM biblioteca')
libros_restantes = cursor.fetchall()
print("\nLibros restantes en la biblioteca:")
for libro in libros_restantes:
    print(libro)

# Cerrar la conexión
conn.close()
