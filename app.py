#tbriyan APP-TAREAS
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
#Configuracion de la base de datos
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "app-tareas"
mysql = MySQL(app)

app.secret_key = "el gato en la caja"

#Rutas
@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM  tarea")
    data = cursor.fetchall()
    print(data)
    return render_template("index.html", tareas = data)

@app.route("/add-tarea", methods=["POST"])
def add_tarea():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO tarea(title, description) VALUES(%s, %s)", (title, description))
        mysql.connection.commit() #se guarda en la base de datos
    return redirect(url_for("index"))

@app.route("/delete-tarea/<string:id>")
def delete_tarea(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM tarea WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for("index"))

@app.route("/edit-tarea/<string:id>")
def edit_tarea(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tarea WHERE id = {0}".format(id))
    data = cursor.fetchall()
    return render_template("edit_tarea.html", tarea = data[0])

@app.route("/update-tarea/<string:id>", methods=["POST"])
def update_tarea(id):
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE tarea SET title = %s, description = %s WHERE id = %s", (title, description, id))
        mysql.connection.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(port=3000, debug=True)