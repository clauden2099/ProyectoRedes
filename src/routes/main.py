from flask import Blueprint, render_template, redirect

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return redirect("/login")

@main_bp.route("/inicio")
def inicio():
    return render_template("inicio.html")
