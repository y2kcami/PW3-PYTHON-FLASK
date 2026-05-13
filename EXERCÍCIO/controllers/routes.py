from flask import render_template, request, redirect, url_for
from models.database import Game, Console, db


def init_app(app):

    listaGames = [{"titulo": "CS-GO", "ano": 2012, "categoria": "FPS Online"}]

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/games')
    def games():
        return render_template('games.html')

    @app.route('/consoles')
    def consoles():
        return render_template('consoles.html')

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

    @app.route('/estoque-jogos', methods=['GET', 'POST'])
    def estoque_jogos():

        if request.method == 'POST':
            dados_form = request.form.to_dict()

            newGame = Game(
                
                dados_form['titulo'],
                int(dados_form['ano']),
                dados_form['categoria'],
                dados_form['plataforma'],
                float(dados_form['preco']),
                int(dados_form['quantidade'])
            )

            db.session.add(newGame)
            db.session.commit()

            return redirect(url_for('estoque_jogos'))

        games = Game.query.all()
        return render_template('estoque-jogos.html', games=games)

    @app.route('/estoque-jogos/delete/<int:id>')
    def delete_game(id):
        game = Game.query.get(id)

        if game:
            db.session.delete(game)
            db.session.commit()

        return redirect(url_for('estoque_jogos'))


    @app.route('/estoque-consoles', methods=['GET', 'POST'])
    def estoque_consoles():

        if request.method == 'POST':
            dados_form = request.form.to_dict()

            newConsole = Console(
                dados_form['nome'],
                dados_form['fabricante'],
                int(dados_form['ano']),
                float(dados_form['preco']),
                int(dados_form['quantidade'])
            )

            db.session.add(newConsole)
            db.session.commit()

            return redirect(url_for('estoque_consoles'))

        consoles = Console.query.all()
        return render_template('estoque-consoles.html', consoles=consoles)

    @app.route('/estoque-consoles/delete/<int:id>')
    def delete_console(id):
        console = Console.query.get(id)

        if console:
            db.session.delete(console)
            db.session.commit()

        return redirect(url_for('estoque_consoles'))

    
    @app.route('/estoque-consoles/edit/<int:id>')
    def edit_console(id):
        console = Console.query.get(id)
        return render_template('edit-console.html', console=console)

    @app.route('/estoque-consoles/update/<int:id>', methods=['POST'])
    def update_console(id):
        console = Console.query.get(id)

        if console:
            console.nome = request.form.get('nome')
            console.fabricante = request.form.get('fabricante')
            console.ano = int(request.form.get('ano'))
            console.preco = float(request.form.get('preco'))
            console.quantidade = int(request.form.get('quantidade'))

            db.session.commit()

        return redirect(url_for('estoque_consoles'))