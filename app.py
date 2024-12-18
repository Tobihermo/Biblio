from flask import Flask, render_template, request

# Definir la clase que manejará la lista
class Lista:
    def __init__(self):
        self.items = []

    def agregar_item(self, item):
        self.items.append(item)

# Crear una instancia de Flask
app = Flask(__name__)

# Crear una instancia de la clase Lista
mi_lista = Lista()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        item = request.form["item"]
        mi_lista.agregar_item(item)  # Agregar el nuevo item a la lista

    # Pasar la lista actualizada a la página
    return render_template("index.html", lista=mi_lista.items)

if __name__ == "__main__":
    app.run(debug=True)
