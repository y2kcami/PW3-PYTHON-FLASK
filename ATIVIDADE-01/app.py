from flask import Flask, render_template 
#render_template RENDERIZA AS PÁGINAS HTML


app = Flask(__name__, template_folder='Views')

@app.route('/')
def home():
    return render_template ("index.html")

@app.route('/lista')
def games():
    return render_template ("lista.html")

@app.route('/forms')
def consoles():
     return render_template ("forms.html")

# INICIANDO O SERVIDOR WEB
if __name__ == '__main__':
    app.run(debug=True)