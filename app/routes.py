from flask import Blueprint, render_template, request, redirect, url_for, session
import csv
import os

main = Blueprint("main", __name__)

# -----------------------------
# Funções auxiliares
# -----------------------------
def init_cart():
    """Garante que o carrinho existe na sessão"""
    if "carrinho" not in session:
        session["carrinho"] = []

def salvar_csv(carrinho):
    """Salva os itens atuais do carrinho em data/carrinho.csv"""
    caminho = os.path.join("data", "carrinho.csv")
    os.makedirs("data", exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo_csv:
        writer = csv.DictWriter(arquivo_csv, fieldnames=["nome", "preco"])
        writer.writeheader()
        for item in carrinho:
            writer.writerow(item)

# -----------------------------
# Rotas principais
# -----------------------------
@main.route("/")
def index():
    init_cart()
    return render_template("index.html")

@main.route("/menu", methods=["GET", "POST"])
def menu():
    init_cart()
    return render_template("menu.html")

@main.route("/about")
def about():
    init_cart()
    return render_template("about.html")

@main.route("/address")
def address():
    init_cart()
    return render_template("address.html")

@main.route("/review")
def review():
    init_cart()
    return render_template("review.html")

@main.route("/cart")
def cart():
    init_cart()
    return render_template("cart.html", carrinho=session["carrinho"])

# -----------------------------
# Carrinho: adicionar/remover
# -----------------------------
@main.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    init_cart()
    nome = request.form.get("nome")
    preco = request.form.get("preco")

    try:
        preco = float(preco)
    except (TypeError, ValueError):
        preco = 0.0

    item = {"nome": nome, "preco": preco}
    session["carrinho"].append(item)
    session.modified = True
    salvar_csv(session["carrinho"])
    return redirect(url_for("main.cart"))

@main.route("/remove_from_cart/<int:index>")
def remove_from_cart(index):
    init_cart()
    try:
        session["carrinho"].pop(index)
        session.modified = True
        salvar_csv(session["carrinho"])
    except IndexError:
        pass
    return redirect(url_for("main.cart"))

# -----------------------------
# Checkout
# -----------------------------
@main.route("/checkout", methods=["GET", "POST"])
def checkout():
    init_cart()
    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")

        itens = "; ".join([f"{item['nome']} (R$ {item['preco']:.2f})" for item in session["carrinho"]])

        caminho = os.path.join("data", "pedidos.csv")
        os.makedirs("data", exist_ok=True)
        arquivo_existe = os.path.exists(caminho)

        with open(caminho, "a", newline="", encoding="utf-8") as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            if not arquivo_existe:
                writer.writerow(["nome", "telefone", "endereco", "itens"])
            writer.writerow([nome, telefone, endereco, itens])

        # limpa carrinho após finalizar
        session["carrinho"] = []
        session.modified = True

        return redirect(url_for("main.index"))

    return render_template("checkout.html", carrinho=session["carrinho"])
