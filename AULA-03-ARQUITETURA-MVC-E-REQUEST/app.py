from flask import Flask, render_template
from controllers import routes
app = Flask(__name__, template_folder='Views')

routes.init_app(app)

# INICIANDO O SERVIDOR
if __name__ == '__main__':
    app.run(debug=True)