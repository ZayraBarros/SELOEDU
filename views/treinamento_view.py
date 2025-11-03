# views/treinamento_view.py
from datetime import datetime
from extensions import db
from models.treinamento import Treinamento

def listar_treinamentos():
    # simples: sem paginação/ordenar
    return Treinamento.query.order_by(Treinamento.id.desc()).all()

def criar_treinamento(form_data: dict):
    """
    form_data: dict vindo do request.form
    Converte datas se vierem preenchidas (formato YYYY-MM-DD).
    """
    def _parse(d):
        if not d:
            return None
        return datetime.strptime(d, "%Y-%m-%d").date()

    novo = Treinamento(
        titulo=form_data.get("titulo", "").strip(),
        descricao=form_data.get("descricao", "").strip() or None,
        carga_horaria=int(form_data.get("carga_horaria") or 0),
        data_inicio=_parse(form_data.get("data_inicio")),
        data_fim=_parse(form_data.get("data_fim")),
        status=form_data.get("status", "ativo"),
    )
    db.session.add(novo)
    db.session.commit()
    return novo
