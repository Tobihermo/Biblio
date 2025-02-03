import os
from flask import Flask, render_template, request, redirect, url_for, flash
from persistencia.reservadao import ReservaDAO
from persistencia.conexion_db import Conexion_Db
from negocio.entidades.usuarios.profesor import Profesor
from negocio.entidades.usuarios.estudiante import Estudiante
from negocio.biblioteca import Biblioteca
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

conexion_db = Conexion_Db()
biblioteca = Biblioteca()
reservadao= ReservaDAO()

def obtener_usuario_por_id(id_usuario):
    with conexion_db.get_db() as conn:
        usuario_row = conn.execute('SELECT * FROM usuarios WHERE id_usuario = ?', (id_usuario,)).fetchone()
        if not usuario_row:
            return None
        
        if usuario_row['tipo'] == 'profesor':
            return Profesor(usuario_row['id_usuario'], usuario_row['nombre'])
        elif usuario_row['tipo'] == 'estudiante':
            return Estudiante(usuario_row['id_usuario'], usuario_row['nombre'])
        return None

def obtener_libros(query=""):
    with conexion_db.get_db() as conn:
        if query:
            return conn.execute(''' 
                SELECT * FROM biblioteca WHERE nombre LIKE ? OR autor LIKE ? 
            ''', (f'%{query}%', f'%{query}%')).fetchall()
        return biblioteca.listar_libros()

def obtener_usuarios():
    with conexion_db.get_db() as conn:
        return conn.execute('SELECT * FROM usuarios').fetchall()

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query", "").strip()
    libros = obtener_libros(query)
    usuarios = obtener_usuarios()

    return render_template("index.html", query=query, libros=libros, usuarios=usuarios)

@app.route("/reservar", methods=["GET", "POST"])
def reservar():
    if request.method == "POST":
        id_libro = request.form.get("id_libro")
        id_usuario = request.form.get("id_usuario")

        if not id_libro or not id_usuario:
            flash('Por favor, selecciona un libro y un usuario.', 'danger')
            return redirect(url_for('reservar'))  # Redirigir a la página de reservas

        usuario = obtener_usuario_por_id(int(id_usuario))
        if not usuario:
            flash('Usuario no encontrado. Por favor, verifica el ID de usuario.', 'danger')
            return redirect(url_for('reservar'))

        libro = biblioteca.buscar_libro_por_id(int(id_libro))
        if not libro:
            flash('Libro no encontrado.', 'danger')
            return redirect(url_for('reservar'))

        exito = biblioteca.prestar_libro(id_libro, id_usuario)
        if exito:
            flash('Reserva realizada con éxito!', 'success')
        else:
            flash('No se pudo realizar la reserva. Verifica la disponibilidad y permisos.', 'danger')

        return redirect(url_for('reservar'))

    # Si es una solicitud GET, se renderiza la página de reservas
    usuarios = obtener_usuarios()
    libros=obtener_libros()
    return render_template("reservas.html", libros=libros, usuarios=usuarios)

@app.route("/devolver", methods=["GET", "POST"])
def devolver():
    if request.method == "POST":
        id_reserva = request.form.get('id_reserva')

        if not id_reserva:
            flash("Por favor, ingresa el ID de la reserva para devolver el libro.", "danger")
            return redirect(url_for('devolver'))  # Redirigir a la página de devoluciones

        try:
            id_reserva = int(id_reserva)
        except ValueError:
            flash("ID de reserva inválido.", "danger")
            return redirect(url_for('devolver'))

        # Usar el ReservaDAO para devolver el libro
        exito = reservadao.devolver_libro(id_reserva)

        if exito:
            flash("Libro devuelto con éxito y reserva eliminada.", "success")
        else:
            flash("No se pudo devolver el libro. Verifica el estado de la reserva.", "danger")

        return redirect(url_for('devolver'))

    # Si es una solicitud GET, se renderiza la página de devoluciones
    libros_reservados = reservadao.listar_reservas()  # Obtener las reservas de libros
    return render_template("devolver_libro.html", libros_reservados=libros_reservados)



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
