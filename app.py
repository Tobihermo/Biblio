import os
from flask import Flask, render_template, request, redirect, url_for, flash
from persistencia.reservadao import ReservaDAO
from persistencia.usuariodao import UsuarioDAO
from persistencia.librodao import LibroDAO
from persistencia.conexion_db import Conexion_Db
from negocio.entidades.usuarios.profesor import Profesor
from negocio.entidades.usuarios.estudiante import Estudiante
from negocio.biblioteca import Biblioteca
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

conexion_db = Conexion_Db()
biblioteca = Biblioteca()
reservadao = ReservaDAO()
usuariodao= UsuarioDAO()
librodao= LibroDAO()


@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query", "").strip()
    libros = librodao.obtener_libros(biblioteca, query)
    usuarios = usuariodao.obtener_usuarios()

    return render_template("index.html", query=query, libros=libros, usuarios=usuarios)


@app.route("/reservar", methods=["GET", "POST"])
def reservar():
    if request.method == "POST":
        id_libro = request.form.get("id_libro")
        id_usuario = request.form.get("id_usuario")

        if not id_libro or not id_usuario:
            flash('Por favor, selecciona un libro y un usuario.', 'danger')
            return redirect(url_for('reservar'))

        usuario = usuariodao.obtener_usuario_por_id(int(id_usuario))
        
        if not usuario:
            flash(
                'Usuario no encontrado. Por favor, verifica el ID de usuario.', 'danger')
            return redirect(url_for('reservar'))

        libro = biblioteca.buscar_libro_por_id(int(id_libro))
        if not libro:
            flash('Libro no encontrado.', 'danger')
            return redirect(url_for('reservar'))

        if usuario.puede_acceder() >= libro.nivel_acceso:
            exito = biblioteca.prestar_libro(id_libro, id_usuario)
            if exito:
                flash('Reserva realizada con éxito!', 'success')
            else:    
                flash('No se pudo realizar la reserva. Verifica la disponibilidad del mismo.', 'danger')
        else:
            flash('Tu usuario no tiene los permisos necesarios para acceder a este libro.', 'danger')


        return redirect(url_for('reservar'))

    usuarios = usuariodao.obtener_usuarios()
    libros = librodao.obtener_libros(biblioteca)
    return render_template("reservas.html", libros=libros, usuarios=usuarios)

@app.route("/devolver", methods=["GET", "POST"])
def devolver():
    if request.method == "POST":
        id_libro = request.form.get('id_libro')

        if not id_libro:
            flash("Por favor, selecciona un libro para devolverlo.", "danger")
            return redirect(url_for('devolver'))

        reserva = reservadao.obtener_reserva_por_id_libro(id_libro)

        if not reserva:
            flash("No se encontró una reserva para ese libro.", "danger")
            return redirect(url_for('devolver'))

        id_reserva = reserva['id_reserva']
        exito = reservadao.devolver_libro(id_reserva)

        if exito:
            flash("Libro devuelto con éxito y reserva eliminada.", "success")
        else:   
            flash("No se pudo devolver el libro. Verifica el estado de la reserva.", "danger")

        return redirect(url_for('devolver'))

    libros_reservados = reservadao.listar_reservas()
    return render_template("devolver_libro.html", libros_reservados=libros_reservados)


@app.route("/historial")
def historial():
    historial = reservadao.obtener_historial()
    return render_template("historial.html", historial=historial)

if __name__ == "__main__":
    app.run(debug=True)