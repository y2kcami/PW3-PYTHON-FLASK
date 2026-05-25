# Importando o render_template
# Motor para renderizar as páginas
from flask import render_template, request, redirect, url_for
#importando o model game e o sqlalchemy
from models.database import Game, Usuario,db
from werkzeug.security import generate_password_hash

# Criando a função para receber o Flask (app)


def init_app(app):
    # SIMULANDO UM BANCO DE DADOS
    listaGames = [{"titulo": "CS-GO", "ano": 2012, "categoria": "FPS Online"}]

    # A partir daqui virão as rotas

    # CRIANDO A ROTA PRINCIPAL DO SITE
    @app.route('/')
    # def serve para criar funções no Python
    def home():
        return render_template('index.html')

    # CRIANDO A ROTA DE GAMES
    @app.route('/games')
    def games():
        # Criando variáveis para passar as informações de um jogo
        titulo = "Silk Song"
        ano = 2025
        categoria = "Metroid Van"

        # Criando um objeto Python (dicionário) para representar as propriedades de um jogo
        game = {
            "Título": "Minecraft",
            "Ano": 2012,
            "Categoria": "Sandbox"
        }
        # Criando vetor (lista)
        jogadores = ['Eduardo', 'Ana', 'Guilherme', 'Vitor', 'Antônio']
        return render_template('games.html',
                               # Enviando as variáveis para página HTML
                               titulo=titulo,
                               ano=ano,
                               categoria=categoria,
                               jogadores=jogadores,
                               game=game)

    # CRIANDO A ROTA DE CONSOLES
    @app.route('/consoles')
    def consoles():
        # Criando vetor (lista)
        consoles = ['Xbox', 'Playstation 5',
                    'Super Nintendo', 'Gameboy', 'Atari']
        return render_template('consoles.html',
                               consoles=consoles)

    # ROTA DE CADASTRO DE JOGOS
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        # Verificando se o método da requisição é POST
        if request.method == 'POST':
            # Recebendo os dados do formulário e gravando na lista
            listaGames.append({'titulo' : request.form.get('titulo'), 'ano' : request.form.get('ano'), 'categoria' : request.form.get('categoria')})
            # o método append() adiciona valores a lista
            return redirect(url_for('cadgames'))    
        return render_template('cadgames.html',
                               listaGames = listaGames)
        
    #ROTA DE ESTOQUE DE JOGOS (CRUD)
    @app.route("/estoque-jogos", methods=['GET','POST'])
    #CRIANDO UM PAREMETRO NA ROTA (ID) PARA EXCLUIR UM REGISTRO
    @app.route("/estoque-jogos/delete/<int:id>")
    def estoque_jogos(id=None):
        #VERIFICANDO SE ESTA SENDO ENVIADO O PARAMETRO ID PARA A ROTA 
        if id:
            game = Game.query.get(id) #SELECT NO BANCO 
            #DELETA O JOGO DO BANCO 
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque_jogos'))
        #VERIFICANDO SE A REQUISIÇÃO É DO TIPO POST 
        if request.method == 'POST':
            #COLETANDO OS DADOS PREENCHIDOS NO FORMULARIO 
            dados_form = request.form.to_dict()
            #ENVIANDO OS DADOS PARA O MODEL
            newGame = Game(
                dados_form['titulo'],
                dados_form['ano'],
                dados_form['categoria'],
                dados_form['plataforma'],
                dados_form['preco'],
                dados_form['quantidade'],
            )
            #METODO DO SQLACHEMY PARA GRAVAR OS DADOS DO BANCO
            db.session.add(newGame)
            #CONFIRMANDO A OPERAÇÃO NO BANCO 
            db.session.commit()
            #REDIRECIONANDO O USUARIO PARA A PAGINA DE ESTOQUE 
            return redirect(url_for('estoque_jogos'))
            
        #SELECIONANDO TODOS OS JOGOS DO BANCO
        #SELECT * FROM GAMES
        games = Game.query.all()
        return render_template('estoque-jogos.html', games=games)
    
    @app.route('/editar-jogos/<int:id>', methods=['GET', 'POST'])
    def editar_jogos(id):
        # BUSCANDO O JOGO NO BANCO PELO ID
        game= Game.query.get(id)
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
      
    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        # VERIFICANDO SE O METODO É POST
        if request.method == "POST":
            # COLETANDO OS DADOS DO FORMULARIO
            email = request.form['email']
            senha = request.form['senha']
            # GERANDO A HASH DA SENHA (CRIPTOGRAFIA)
            senha_criptografada = generate_password_hash(senha, method='scrypt')
            
            # ENVIANDO OS DADOS PARA O MODEL
            novo_usuario = Usuario(email=email, senha=senha_criptografada)
            # CADASTRANDO NO BANCO 
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('cadastro.html')
    
    @app.route('/login' , methods=['GET', 'POST'])
    def login():
        return "Bem-vindo a página de login"
    