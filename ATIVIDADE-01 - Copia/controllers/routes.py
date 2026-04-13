# IMPORTANDO
from flask import render_template, request, redirect, url_for

def init_app(app):

    listaFilmes = [
        {"nome": "Interestelar", "ano": 2014, "genero": "Ficção Científica", "nota": 10, "duracao": "2h49min"},
        {"nome": "A Barraca do Beijo", "ano": 2018, "genero": "Romance", "nota": 8, "duracao": "1h45min"},
        {"nome": "Para Todos os Garotos que Já Amei", "ano": 2018, "genero": "Romance", "nota": 8, "duracao": "1h39min"}
    ]

    @app.route('/')
    def home():
        return render_template("index.html")

    # ROTA FILMES
    @app.route('/filmes')
    def filmes_page():
        
        nome = "Interestelar"
        ano = 2014
        genero = "Ficção Científica"
        nota = 10
        duracao = "2h49min"
        
        espectadores = ['Ana', 'Carlos', 'Beatriz', 'João', 'Lucas']
        
        filme = {
            "Nome": "Interestelar",
            "Ano": 2014,
            "Gênero": "Ficção Científica",
            "Nota": 10,
            "Duração": "2h49min"
        }
        
        return render_template(
            "filmes.html",
            nome=nome,
            ano=ano,
            genero=genero,
            nota=nota,
            duracao=duracao,
            espectadores=espectadores,
            filme=filme,
            listaFilmes=listaFilmes  # 🔥 importante se usar tabela
        )

    # CADASTRO FILMES
    @app.route('/cadfilmes', methods=['GET', 'POST'])
    def cadfilmes():

        if request.method == 'POST':
            listaFilmes.append({
                'nome': request.form.get('nome'),
                'ano': request.form.get('ano'),
                'genero': request.form.get('genero'),
                'nota': request.form.get('nota'),
                'duracao': request.form.get('duracao')
            })
            return redirect(url_for('cadfilmes'))

        return render_template("cadfilmes.html", listaFilmes=listaFilmes)