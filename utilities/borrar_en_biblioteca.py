import sqlite3

conn = sqlite3.connect('data/biblioteca.db')
cursor = conn.cursor()

def borrar_libro():
    print("Ingrese el ID del libro que desea borrar:")
    id_libro = int(input("ID del libro: "))
    
    cursor.execute('SELECT * FROM biblioteca WHERE id_libro = ?', (id_libro,))
    libro = cursor.fetchone()
    
    if libro:
        print(f"\nLibro encontrado: {libro}")
        confirmacion = input("¿Está seguro de que desea borrar este libro? (s/n): ")
        
        if confirmacion.lower() == 's':
            cursor.execute('DELETE FROM biblioteca WHERE id_libro = ?', (id_libro,))
            conn.commit()
            print("Libro borrado exitosamente.")
        else:
            print("Operación cancelada.")
    else:
        print("No se encontró un libro con ese ID.")

def borrar_varios_libros(cantidad):
    for i in range(cantidad):
        print(f"\nBorrando libro {i+1} de {cantidad}...")
        borrar_libro()

cantidad_libros = int(input("¿Cuántos libros desea borrar? "))
borrar_varios_libros(cantidad_libros)

cursor.execute('SELECT * FROM biblioteca')
libros_restantes = cursor.fetchall()
print("\nLibros restantes en la biblioteca:")
for libro in libros_restantes:
    print(libro)

conn.close()
