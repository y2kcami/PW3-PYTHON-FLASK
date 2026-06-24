# Importando o Flask para a aplicação
from flask import render_template, request, redirect, url_for, flash
# Importando o Model de Games
from markupsafe import Markup
from models.database import Game, db, Usuario
# Importando WERKZEUG
from werkzeug.security import generate_password_hash

# Criando a função principal para inicializar as rotas


def init_app(app):
    # VARIÁVEIS GLOBAIS
    listaConsoles = ['Playstation 5', 'Xbox One',
                     'Super Nintendo', 'Atari', '3DS']

    listaGames = [{"titulo": "CS-GO", "ano": 2012,
                   "categoria": "FPS Online", "plataforma": "PC (Windows)"}]

    # CRIANDO A ROTA PRINCIPAL DO SITE
    @app.route('/')
    # def cria funções no Python
    def home():
        return render_template('index.html')

    @app.route('/games')
    def games():
        # Criando variáveis para a rota de games
        titulo = "Portal 2"
        ano = 2011
        categoria = "Puzzle"
        # Lista de jogadores (uma lista é um vetor/array)
        jogadores = ['Marcos', 'Richard', 'Miguel', 'Renato', 'Pedro']
        # Enviando as variáveis para o HTML
        return render_template('games.html',
                               titulo=titulo,
                               ano=ano,
                               categoria=categoria,
                               jogadores=jogadores)

    @app.route('/consoles', methods=['GET', 'POST'])
    def consoles():
        # Criando um objeto
        console = {"Nome": "Playstation 2",
                   "Fabricante": "Sony",
                   "Ano": 2000}

        # Recendo o valor do formulário
        if request.method == 'POST':
            if request.form.get('novoConsole'):
                listaConsoles.append(request.form.get('novoConsole'))

        return render_template('consoles.html',
                               console=console,
                               listaConsoles=listaConsoles)

    # ROTA PARA CADASTRAR UM JOGO
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():

        # Recebendo os dados do formulário e enviando para página
        # Verificando se a requisição do usuário é do tipo POST
        if request.method == 'POST':
            # Aqui ele irá gravar os dados na lista de jogos
            listaGames.append({'titulo': request.form.get('titulo'), 'ano': request.form.get(
                'ano'), 'categoria': request.form.get('categoria'), 'plataforma': request.form.get('plataforma')})
            # Aqui o usuário será redirecionado novamente para a página
            return redirect(url_for('cadgames'))
        return render_template('cadgames.html',
                               listaGames=listaGames)

    # ROTA PARA O CRUD (ESTOQUE DE JOGOS)
    @app.route('/estoque', methods=['GET', 'POST'])
    # ADICIONANDO O PARÂMETRO ID A ROTA
    @app.route('/estoque/delete/<int:id>')    
    def estoque(id=None):
        # VERIFICANDO SE O ID FOI PASSADO PARA ROTA
        if id:
            game = Game.query.get(id) # SELECIONA O JOGO
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))
            
        # CONDIÇÃO PARA VERIFICAR SE O USUÁRIO ESTÁ ENVIANDO UMA REQUISIÇÃO POST (cadastro)
        if request.method == 'POST':
            # REALIZA O CADASTRO
            # COLETANDO OS DADOS DO FORMULÁRIO
            # Pega os dados do formulário e transforma em um dicionário (objeto)
            dados = request.form.to_dict()
            # Enviando os dados para o Model
            newgame = Game(
                dados['titulo'],
                dados['ano'],
                dados['categoria'],
                dados['plataforma'],
                dados['preco'],
                dados['quantidade']
            )
            # Método do SQLAlchemy para gravar no banco
            db.session.add(newgame)
            # Confirmação
            db.session.commit()  
            return redirect(url_for('estoque'))      
        # SELECIONANDO TODOS OS JOGOS DA TABELA
        games = Game.query.all()
        return render_template('estoque.html', games=games)

    @app.route('/estoque/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        # Selecionando o jogo no banco pelo ID
        game = Game.query.get(id)
        # Verificando se a requisição é POST
        if request.method == 'POST':
            dados_form = request.form.to_dict()
            # Alterando os dados do jogo
            game.titulo = dados_form['titulo']
            game.ano = dados_form['ano']
            game.categoria = dados_form['categoria']
            game.plataforma = dados_form['plataforma']
            game.preco = dados_form['preco']
            game.quantidade = dados_form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editGame.html', game=game)
    
    # ROTA DE CADASTRO DE USUARIO
    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        # Verificando se o método é POST
        if request.method == 'POST':
            # Coletando os dados do Formulário
            email = request.form['email']
            senha = request.form['senha']
            # VERIFICANDO SE O USUARIO JA EXISTE E BUSCANDO O USUARIO PELO EMAIL
            usuario = Usuario.query.filter_by(email=email).first()
            # VERFICANDO SE O USUARIO TEM VALOR
            if usuario:
                msg= Markup("Usuario ja cadastrado. Faça o <a href='login'>login</a")
                flash(msg, 'danger')
                return redirect(url_for('cadastro'))
            
            # GERANDO O HASH DA SENHA (CRIPTOGRAFIA)
            senha_criptografada = generate_password_hash(senha, method='scrypt')            
            # Enviando os dados para o Model
            novo_usuario = Usuario(email=email, senha=senha_criptografada)
            # Cadastrando no banco
            db.session.add(novo_usuario)
            db.session.commit()
            # GERANDO A MENSAGEM DE SUCESSO
            msgCad=Markup("Cadastro realizado com sucesso! Faça o <a href='/login'>login</>")
            flash(msgCad, 'success')
            return redirect(url_for('cadastro'))        
        return render_template('cadastro.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return render_template('login.html')
    