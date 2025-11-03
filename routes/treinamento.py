# routes/treinamento.py
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from views.treinamento_view import listar_treinamentos, criar_treinamento

treinamento_bp = Blueprint("treinamento", __name__, url_prefix="/treinamentos")

def _is_coordenador(user) -> bool:
    # aceita tanto .perfil ("coordenador") quanto .role ("coordenador")
    role = getattr(user, "role", None) or getattr(user, "perfil", "")
    return (role or "").lower() == "coordenador"

@treinamento_bp.get("/")
@login_required
def listar():
    itens = listar_treinamentos()
    return render_template("treinamento/listar.html", treinamentos=itens)

@treinamento_bp.get("/novo")
@login_required
def novo_form():
    if not _is_coordenador(current_user):
        # somente coordenador pode ver/cadastrar
        abort(403)
    return render_template("treinamento/novo.html")

@treinamento_bp.post("/novo")
@login_required
def novo_post():
    if not _is_coordenador(current_user):
        abort(403)
    criar_treinamento(request.form)
    # sem estilização, só feedback mínimo
    flash("Treinamento criado com sucesso.")
    return redirect(url_for("treinamento.listar"))
