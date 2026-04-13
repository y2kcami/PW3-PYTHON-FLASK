from flask import Flask
from controllers import routes

app = Flask(__name__, template_folder='Views')

routes.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)