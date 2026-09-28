from flask import render_template, request, redirect, url_for, session, flash
from models.database import Game, db, Console, Usuario
from werkzeug.security import generate_password_hash, check_password_hash


def init_app(app):

    listaConsoles = ['Playstation 5', 'Xbox One',
                     'Super Nintendo', 'Atari', '3DS']

    listaGames = [{
        "titulo": "CS-GO",
        "ano": 2012,
        "categoria": "FPS Online",
        "plataforma": "PC (Windows)"
    }]

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/games')
    def games():
        titulo = "Portal 2"
        ano = 2011
        categoria = "Puzzle"
        jogadores = ['Marcos', 'Richard', 'Miguel', 'Renato', 'Pedro']

        return render_template(
            'games.html',
            titulo=titulo,
            ano=ano,
            categoria=categoria,
            jogadores=jogadores
        )

    @app.route('/consoles', methods=['GET', 'POST'])
    def consoles():
        console = {
            "Nome": "Playstation 2",
            "Fabricante": "Sony",
            "Ano": 2000
        }

        if request.method == 'POST':
            if request.form.get('novoConsole'):
                listaConsoles.append(request.form.get('novoConsole'))

        return render_template(
            'consoles.html',
            console=console,
            listaConsoles=listaConsoles
        )

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():

        if request.method == 'POST':
            listaGames.append({
                'titulo': request.form.get('titulo'),
                'ano': request.form.get('ano'),
                'categoria': request.form.get('categoria'),
                'plataforma': request.form.get('plataforma')
            })

            return redirect(url_for('cadgames'))

        return render_template(
            'cadgames.html',
            listaGames=listaGames
        )

    @app.route('/estoque', methods=['GET', 'POST'])
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):

        if id:
            game = Game.query.get(id)
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))

        if request.method == 'POST':
            dados = request.form.to_dict()

            newgame = Game(
                dados['titulo'],
                dados['ano'],
                dados['categoria'],
                dados['plataforma'],
                dados['preco'],
                dados['quantidade']
            )

            db.session.add(newgame)
            db.session.commit()

            return redirect(url_for('estoque'))

        games = Game.query.all()

        return render_template(
            'estoque.html',
            games=games
        )

    @app.route('/estoque/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):

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

            return redirect(url_for('estoque'))

        return render_template(
            'editGame.html',
            game=game
        )

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():

        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']

            senha_com_hash = generate_password_hash(
                senha,
                method='scrypt'
            )

            novo_usuario = Usuario(
                email=email,
                senha=senha_com_hash
            )

            db.session.add(novo_usuario)
            db.session.commit()

            return redirect(url_for('login'))

        return render_template('cadastro.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():

        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']

            usuario = Usuario.query.filter_by(email=email).first()

            if usuario:
                if check_password_hash(usuario.senha, senha):
                    session['usuario_id'] = usuario.id
                    session['usuario_email'] = usuario.email

                    flash(
                        'Você foi autenticado com sucesso! Bem-vindo!',
                        'success'
                    )

                    return redirect(url_for('home'))

                flash(
                    'Falha no login. Verifique os dados e tente novamente!',
                    'danger'
                )

                return redirect(url_for('login'))

            flash(
                'O usuário informado não existe!',
                'danger'
            )

            return redirect(url_for('login'))

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))