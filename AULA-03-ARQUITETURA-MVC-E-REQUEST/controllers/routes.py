# IMPORTANDO RENDER_TEMPLATE
from flask import render_template

# CRIANDO A FUNÇÃO PARA RECEBER O FLASK (APP)
def init_app(app):

    # ROTA HOME
    @app.route('/')
    def home():
        return render_template("index.html")

    # ROTA GAMES
    @app.route('/games')
    def games_page():
        
        # Criando variáveis
        titulo = "Silk Song"
        ano = 2025
        categoria = "Metroidvania"
        
        jogadores = ['Eduardo', 'Ana', 'Guilherme', 'Victor', 'William']
        
        games = {
            "Título": "Hollow Knight: Silksong",
            "Ano": 2025,
            "Categoria": "Metroidvania"
        }
        
        # Enviando para o HTML
        return render_template(
            "games.html",
            titulo=titulo,
            ano=ano,
            categoria=categoria,
            jogadores=jogadores,
            games=games
        )

    # ROTA CONSOLES
    @app.route('/consoles')
    def consoles():
        
        game = {
            "Título": "Minecraft",
            "Ano": 2012,
            "Categoria": "Sandbox"
        }
        
        jogadores = ['Eduardo', 'Ana', 'Guilherme', 'Victor', 'William']

        # Vetor de consoles
        consoles_lista = ['PlayStation 5', 'Xbox Series X', 'Nintendo Switch', 'PC Gamer']
        
        return render_template(
            "consoles.html",
            jogadores=jogadores,
            game=game,
            consoles=consoles_lista
        )