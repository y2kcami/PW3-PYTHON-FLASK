from flask import render_template, request, redirect, url_for, flash
from markupsafe import Markup
from models.database import Game, Usuario, db
from werkzeug.security import generate_password_hash
import os

def init_app(app):

    # CONFIGURAÇÃO DE SEGURANÇA
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

    # SIMULANDO UM BANCO DE DADOS
    listaGames = [{"titulo": "CS-GO", "ano": 2012, "categoria": "FPS Online"}]

    #ROTAS 

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/games')
    def games():
        titulo = "Silk Song"
        ano = 2025
        categoria = "Metroid Van"

        game = {
            "Título": "Minecraft",
            "Ano": 2012,
            "Categoria": "Sandbox"
        }

        jogadores = ['Eduardo', 'Ana', 'Guilherme', 'Vitor', 'Antônio']

        return render_template('games.html',
                               titulo=titulo,
                               ano=ano,
                               categoria=categoria,
                               jogadores=jogadores,
                               game=game)

    @app.route('/consoles')
    def consoles():
        consoles = ['Xbox', 'Playstation 5', 'Super Nintendo', 'Gameboy', 'Atari']
        return render_template('consoles.html', consoles=consoles)

    #CADASTRO SIMPLES

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            listaGames.append({
                'titulo': request.form.get('titulo'),
                'ano': request.form.get('ano'),
                'categoria': request.form.get('categoria')
            })
            return redirect(url_for('cadgames'))

        return render_template('cadgames.html', listaGames=listaGames)

    #CRUD (BANCO)

    @app.route("/estoque-jogos", methods=['GET', 'POST'])
    def estoque_jogos():

        if request.method == 'POST':
            dados_form = request.form.to_dict()

            newGame = Game(
                dados_form['titulo'],
                dados_form['ano'],
                dados_form['categoria'],
                dados_form['plataforma'],
                dados_form['preco'],
                dados_form['quantidade'],
            )

            db.session.add(newGame)
            db.session.commit()

            return redirect(url_for('estoque_jogos'))

        games = Game.query.all()
        return render_template('estoque-jogos.html', games=games)

    #ROTA SEPARADA PARA DELETAR 
    @app.route("/estoque-jogos/delete/<int:id>")
    def deletar_jogo(id):
        game = Game.query.get(id)

        if game:
            db.session.delete(game)
            db.session.commit()

        return redirect(url_for('estoque_jogos'))

    #EDITAR 

    @app.route('/editar-jogos/<int:id>', methods=['GET', 'POST'])
    def editar_jogos(id):
        game = Game.query.get(id)

        if request.method == 'POST':
            dados_form = request.form.to_dict()

            game.titulo = dados_form['titulo']
            game.ano = dados_form['ano']
            game.categoria = dados_form['categoria']
            game.plataforma = dados_form['plataforma']
            game.preco = dados_form['preco']
            game.quantidade = dados_form['quantidade']

            db.session.commit()
            return redirect(url_for('estoque_jogos'))

        return render_template('editar-jogos.html', game=game)

    #CADASTRO DE USUÁRIO 

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():

        if request.method == "POST":
            email = request.form['email']
            senha = request.form['senha']

            usuario = Usuario.query.filter_by(email=email).first()

            if usuario:
                flash(Markup('E-mail já cadastrado. <a href="/login">Faça login</a>'), 'error')
                return redirect(url_for('cadastro'))

            senha_criptografada = generate_password_hash(senha)

            novo_usuario = Usuario(email=email, senha=senha_criptografada)

            db.session.add(novo_usuario)
            db.session.commit()

            flash(Markup('Cadastro realizado com sucesso. <a href="/login">Faça login</a>'), 'success')

            return redirect(url_for('cadastro'))

        return render_template('cadastro.html')

    #LOGIN

    @app.route('/login', methods=['GET', 'POST'])
    def login():
         return render_template('login.html')