
from datetime import date
from extensions import db  # já existe no projeto

class Treinamento(db.Model):
    __tablename__ = "treinamentos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    carga_horaria = db.Column(db.Integer, nullable=False, default=0)
    data_inicio = db.Column(db.Date, nullable=True)
    data_fim = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="ativo")  # ativo/inativo

    def __repr__(self):
        return f"<Treinamento {self.id} - {self.titulo}>"
