from flask import Flask, render_template, request

# Crear una instancia de Flask
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    if request.method == "POST":
        # Obtener la consulta desde el formulario
        query = request.form.get("query", "")
    # Renderizar la plantilla con la consulta (si existe)
    return render_template("index.html", query=query)

if __name__ == "__main__":  
    app.run(debug=True)
