from flask import render_template, request, redirect, url_for, redirect, flash, session
from models.database import Game, db, Console, Usuario
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.request 
import json  
import os
import uuid


def init_app(app):
    @app.before_request
    def check_auth():
        rotasPermitidas = ['home', 'login', 'cadastro', 'static']
        if request.endpoint in rotasPermitidas:
            return
        if 'usuario_id' not in session:
            return redirect(url_for('login'))

    listaConsoles = ['Playstation 5', 'Xbox One',
                     'Super Nintendo', 'Atari', '3DS']

    listaGames = [{"titulo": "CS-GO", "ano": 2012,
                   "categoria": "FPS Online", "plataforma": "PC (Windows)"}]

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/games')
    def games():
        titulo = "Portal 2"
        ano = 2011
        categoria = "Puzzle"
        jogadores = ['Marcos', 'Richard', 'Miguel', 'Renato', 'Pedro']
        return render_template('games.html',
                               titulo=titulo,
                               ano=ano,
                               categoria=categoria,
                               jogadores=jogadores)

    @app.route('/consoles', methods=['GET', 'POST'])
    def consoles():
        console = {"Nome": "Playstation 2",
                   "Fabricante": "Sony",
                   "Ano": 2000}

        if request.method == 'POST':
            if request.form.get('novoConsole'):
                listaConsoles.append(request.form.get('novoConsole'))

        return render_template('consoles.html',
                               console=console,
                               listaConsoles=listaConsoles)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        
        if request.method == 'POST':
            listaGames.append({'titulo': request.form.get('titulo'), 'ano': request.form.get(
                'ano'), 'categoria': request.form.get('categoria'), 'plataforma': request.form.get('plataforma')})
            return redirect(url_for('cadgames'))
        return render_template('cadgames.html',
                               listaGames=listaGames)

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
        return render_template('estoque.html', games=games)

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
        return render_template('editGame.html', game=game)

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            senha_com_hash = generate_password_hash(senha, method='scrypt')
            novo_usuario = Usuario(email=email, senha=senha_com_hash)
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('cadastro.html')

    # ROTA DE LOGIN
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
                    msgLogin = "Você foi autenticado com sucesso! Bem-vindo!"
                    flash(msgLogin, 'success')
                    return redirect(url_for('home'))
                else:
                    flash(
                        'Falha no login. Verifique os dados e tente novamente!', 'danger')
                    return redirect(url_for('login'))
            else:
                flash('O usuário informado não existe!', 'danger')
                return redirect(url_for('login'))
        return render_template('login.html')

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session.clear()
        return redirect(url_for('home'))

    # ROTA DE CONSUMO DA API
    @app.route('/apigames', methods=['GET', 'POST'])
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        urlAPI = 'https://www.freetogame.com/api/games'
        resposta = urllib.request.urlopen(urlAPI)
        dados = resposta.read()
        listaJogos = json.loads(dados)
        if id:
            jogoInfo = []
            for jogo in listaJogos:
                if jogo['id'] == id:
                    jogoInfo = jogo
                    break
            if jogoInfo:
                return render_template('gameinfo.html', jogoInfo=jogoInfo)
            else:
                return f'Jogo com a ID {id} não foi encontrado.'
        else:
            return render_template('apigames.html', listaJogos=listaJogos)
        
    # ROTA DE UPLOAD
    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        
        # LISTA DE EXTENSÕES
        FILE_TYPES = set(['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'])
        # VALIDAR O TIPO DE ARQUIVO ENVIADO
        
        def arquivos_permitidos(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES 
        
        # RECEBENDO O ARQUIVO DO FORMULÁRIO
        if request.method == 'POST':
            
            # GUARDO O ARQUIVO
            file = request.files['file']
            
            # Verificar se a extensão é válida
            if not arquivos_permitidos(file.filename):
                flash("Arquivo não permitido! Envie somente arquivos de imagem.", 'danger')
                return redirect(request.url)
            
            # SE A EXTENSÃO FOR VÁLIDA
            filename = str(uuid.uuid4())
            
            # Salva o arquivo 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
            flash("Imagem recebida com sucesso!", 'success')
            return redirect(url_for('galeria'))      
        return render_template('galeria.html')
