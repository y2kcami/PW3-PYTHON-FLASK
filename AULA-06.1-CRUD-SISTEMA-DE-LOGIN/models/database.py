# Importando o SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabela Game
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    titulo = db.Column(db.String(150))
    ano = db.Column(db.Integer)
    categoria = db.Column(db.String(150))
    plataforma = db.Column(db.String(150))
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)

    def __init__(self, titulo, ano, categoria, plataforma, preco, quantidade):
        self.titulo = titulo
        self.ano = ano
        self.categoria = categoria
        self.plataforma = plataforma
        self.preco = preco
        self.quantidade = quantidade


# Tabela Usuario (SEPARADA)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def __init__(self, email, senha):
        self.email = email
        self.senha = senha