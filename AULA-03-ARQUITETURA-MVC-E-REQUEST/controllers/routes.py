# IMPORTANDO RENDER_TEMPLATE
from flask import render_template,request,redirect,url_for


# CRIANDO A FUNÇÃO PARA RECEBER O FLASK (APP)
def init_app(app):

    # SIMULANDO UM BD
    listaGames = [
        {"titulo": "CS-GO", "ano": 2012, "categoria": "FPS Online"}
    ]

    # ROTA HOME
    @app.route('/')
    def home():
        return render_template("index.html")

    # ROTA GAMES
    @app.route('/games')
    def games_page():
        
        titulo = "Silk Song"
        ano = 2025
        categoria = "Metroidvania"
        
        jogadores = ['Eduardo', 'Ana', 'Guilherme', 'Victor', 'William']
        
        games = {
            "Título": "Hollow Knight: Silksong",
            "Ano": 2025,
            "Categoria": "Metroidvania"
        }
        
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

        consoles_lista = ['PlayStation 5', 'Xbox Series X', 'Nintendo Switch', 'PC Gamer']
        
        return render_template(
            "consoles.html",
            jogadores=jogadores,
            game=game,
            consoles=consoles_lista
        )
    # ROTA DE CADASTRO DE JOGOS
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():

        # VERIFICANDO SE É POST
        if request.method == 'POST':

            listaGames.append({
                'titulo': request.form.get('titulo'),
                'ano': request.form.get('ano'),
                'categoria': request.form.get('categoria')
            })

            return redirect(url_for('cadgames'))

        return render_template(
            "cadgames.html",
            listaGames = listaGames
        )