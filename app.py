from flask import Flask, render_template

app = Flask(__name__)

# Página principal (landing page - single page)
@app.route("/")
def index():
    return render_template("index.html")

# Páginas individuais (multi page)
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/review")
def review():
    return render_template("review.html")

@app.route("/address")
def address():
    return render_template("address.html")

