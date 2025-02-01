from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
from persistencia.reservadao import ReservaDAO
from persistencia.conexion_db import Conexion_Db
from negocio.entidades.usuarios.profesor import Profesor
from negocio.entidades.usuarios.estudiante import Estudiante
from negocio.biblioteca import Biblioteca

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conexion_db=Conexion_Db()
biblioteca=Biblioteca()

def obtener_usuario_por_id(id_usuario):
    with conexion_db.get_db() as conn:
        usuario_row = conn.execute('SELECT * FROM usuarios WHERE id_usuario = ?', (id_usuario,)).fetchone()
        if not usuario_row:
            return None
        
        # Crear instancia de usuario según el tipo
        if usuario_row['tipo'] == 'profesor':
            return Profesor(usuario_row['id_usuario'], usuario_row['nombre'])
        elif usuario_row['tipo'] == 'estudiante':
            return Estudiante(usuario_row['id_usuario'], usuario_row['nombre'])
        else:
            return None



# Página principal con búsqueda de libros
@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query", "").strip() 
    libros = []

    # Si hay una consulta (búsqueda), filtrar los libros según la consulta
    if query:
        with conexion_db.get_db() as conn:
            # Aquí deberías hacer una búsqueda en la base de datos por el nombre o autor del libro
            libros = conn.execute('''
                SELECT * FROM biblioteca WHERE nombre LIKE ? OR autor LIKE ?
            ''', (f'%{query}%', f'%{query}%')).fetchall()
    else:
        # Si no hay consulta, mostrar todos los libros
        libros = biblioteca.listar_libros()

    return render_template("index.html", query=query, libros=libros)


# Página de reservas (prestar libros)
@app.route("/reservar", methods=["GET", "POST"])
def reservar():
    if request.method == "POST":
        id_libro = request.form.get("id_libro")
        id_usuario = request.form.get("id_usuario")


        # Validación simplificada
        if not id_libro or not id_usuario:
            flash('Por favor, selecciona un libro y un usuario.', 'danger')
            return redirect(url_for('reservar'))

        usuario = obtener_usuario_por_id(int(id_usuario))
        if not usuario:
            flash('Usuario no encontrado. Por favor, verifica el ID de usuario.', 'danger')
            return redirect(url_for('reservar'))

        libro = biblioteca.buscar_libro_por_id(int(id_libro))
        if not libro:
            flash('Libro no encontrado.', 'danger')
            return redirect(url_for('reservar'))

        # Realizar la reserva utilizando la capa de negocio
        exito = biblioteca.prestar_libro(id_libro, id_usuario)
        if exito:
            flash('Reserva realizada con éxito!', 'success')
        else:
            flash('No se pudo realizar la reserva. Verifica la disponibilidad y permisos.', 'danger')

        return redirect(url_for('reservar'))

    # Mostrar usuarios y libros
    with conexion_db.get_db() as conn:
        usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
        libros = conn.execute('SELECT * FROM BIBLIOTECA').fetchall()
    return render_template("reservas.html", libros=libros, usuarios=usuarios)



@app.route('/devolver_libro', methods=['GET', 'POST'])
def devolver():
    if request.method == 'POST':
        id_reserva = request.form.get('id_reserva')

        if not id_reserva:  
            flash("Por favor, ingrese un ID de reserva.", "danger")
            return redirect(url_for('devolver'))

        with conexion_db.get_db() as conn:
            # Buscar la reserva y obtener el id_libro asociado
            reserva = conn.execute('SELECT * FROM reservas WHERE id_reserva = ?', (id_reserva,)).fetchone()

            if reserva:
                id_libro = reserva['id_libro'] 
                # Eliminar la reserva
                conn.execute('DELETE FROM reservas WHERE id_reserva = ?', (id_reserva,))
                # Actualizar el estado del libro a 'disponible'
                conn.execute('UPDATE biblioteca SET estado = "disponible" WHERE id_libro = ?', (id_libro,))
                
                conn.commit()
                flash(f"Reserva {id_reserva} devuelta con éxito.", "success")
            else:
                flash(f"No se encontró la reserva con ID {id_reserva}.", "danger")

        return redirect(url_for('devolver'))

    return render_template('devolver_libro.html')




# Página para ver el historial de préstamos
@app.route("/historial")
def historial():
    with conexion_db.get_db() as conn:
        historial = conn.execute(''' 
            SELECT * FROM reservas
            JOIN biblioteca ON reservas.id_libro = biblioteca.id_libro
            JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario
            ORDER BY reservas.fecha_reserva DESC
        ''').fetchall()

    return render_template("historial.html", historial=historial)

if __name__ == "__main__":
    app.run(debug=True)
