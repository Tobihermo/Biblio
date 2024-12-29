from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
from persistencia.reservadao import ReservaDAO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db():
    conn = sqlite3.connect('data/biblioteca.db')
    conn.row_factory = sqlite3.Row
    return conn

def obtener_usuario_por_id(id_usuario):
    with get_db() as conn:
        usuario = conn.execute('SELECT * FROM usuarios WHERE id_usuario = ?', (id_usuario,)).fetchone()
        return usuario

def obtener_libros_disponibles(nivel_acceso):
    with get_db() as conn:
        libros = conn.execute(''' 
            SELECT * FROM biblioteca 
            WHERE estado = "disponible" AND nivel_acceso <= ?
        ''', (nivel_acceso,)).fetchall()
        return libros

# Página principal con búsqueda de libros
@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query", "")  # Obtener la consulta del formulario si hay alguna
    libros = []

    # Si hay una consulta (búsqueda), filtrar los libros según la consulta
    if query:
        with get_db() as conn:
            libros = conn.execute('''
                SELECT * FROM biblioteca 
                WHERE nombre LIKE ? OR autor LIKE ? OR categoria LIKE ?
            ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%')).fetchall()
    else:
        # Si no hay consulta, no mostrar libros por defecto, solo mostrar el formulario
        libros = []

    return render_template("index.html", query=query, libros=libros)

# Página de reservas (prestar libros)
@app.route("/reservar", methods=["GET", "POST"])
def reservar():
    if request.method == "POST":
        id_libro = request.form.get("id_libro")
        id_usuario = request.form.get("id_usuario")

        if 'devolver' in request.form:
            id_reserva = request.form.get('id_reserva')
            reserva_dao = ReservaDAO()
            reserva_dao.devolver_libro(id_reserva)
            flash('Libro devuelto con éxito!', 'success')
            return redirect(url_for('index'))


        # Validación de datos más robusta
        if not id_libro:
            flash('Por favor, selecciona un libro.', 'danger')
            return redirect(url_for('reservar'))
        if not id_usuario:
            flash('Por favor, selecciona un usuario.', 'danger')
            return redirect(url_for('reservar'))

        # Obtener el nivel de acceso del usuario y los detalles del libro
        usuario = obtener_usuario_por_id(id_usuario)
        if not usuario:
            flash('Usuario no encontrado. Por favor, verifica el ID de usuario.', 'danger')
            return redirect(url_for('reservar'))

        with get_db() as conn:
            libro = conn.execute('SELECT * FROM biblioteca WHERE id_libro = ?', (id_libro,)).fetchone()
            if not libro:
                flash('Libro no encontrado.', 'danger')
                return redirect(url_for('reservar'))

        # Verificar disponibilidad y nivel de acceso
        print(libro)  # Depuración: Ver el libro y su estado
        if libro and libro['estado'] == 'disponible' and libro['nivel_acceso'] <= usuario['nivel_acceso']:
            # Crear la reserva y actualizar el estado del libro
            fecha_reserva = datetime.now()
            fecha_devolucion = fecha_reserva.replace(year=fecha_reserva.year + 1)  # Ejemplo: 1 año de duración

            # Insertar la reserva en la base de datos
            with get_db() as conn:
                conn.execute('''INSERT INTO reservas (id_libro, id_usuario, fecha_reserva, fecha_devolucion) 
                                VALUES (?, ?, ?, ?)''', 
                             (id_libro, id_usuario, fecha_reserva, fecha_devolucion))
                conn.execute('UPDATE biblioteca SET estado = "prestado" WHERE id_libro = ?', (id_libro,))
                conn.commit()

            flash('Reserva realizada con éxito!', 'success')
        else:
            if libro['estado'] != 'disponible':
                flash('Este libro ya está prestado.', 'danger')
            else:
                flash('No tienes permiso para reservar este libro.', 'danger')
            return redirect(url_for('reservar'))

    # Obtener los libros disponibles para el usuario logueado
    usuario_actual = obtener_usuario_por_id(1)  # Asumimos que el ID del usuario está disponible (ajustar según tu lógica)
    libros = obtener_libros_disponibles(usuario_actual['nivel_acceso'])

    with get_db() as conn:
        usuarios = conn.execute('SELECT * FROM usuarios').fetchall()

    return render_template("reservas.html", libros=libros, usuarios=usuarios)

# Página para renovar una reserva
@app.route("/renovar/<int:id_reserva>", methods=["POST"])
def renovar_reserva(id_reserva):
    with get_db() as conn:
        reserva = conn.execute('SELECT * FROM reservas WHERE id_reserva = ?', (id_reserva,)).fetchone()
        if reserva:
            nueva_fecha_devolucion = datetime.now().replace(year=datetime.now().year + 1)
            conn.execute('UPDATE reservas SET fecha_devolucion = ? WHERE id_reserva = ?', 
                         (nueva_fecha_devolucion, id_reserva))
            conn.commit()
            flash('Reserva renovada con éxito!', 'success')
        else:
            flash('Reserva no encontrada.', 'danger')

    return redirect(url_for('index'))

# Página para ver el historial de préstamos
@app.route("/historial")
def historial():
    with get_db() as conn:
        historial = conn.execute(''' 
            SELECT * FROM reservas
            JOIN biblioteca ON reservas.id_libro = biblioteca.id_libro
            JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario
            ORDER BY reservas.fecha_reserva DESC
        ''').fetchall()

    return render_template("historial.html", historial=historial)

if __name__ == "__main__":
    app.run(debug=True)
