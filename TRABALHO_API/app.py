from flask import Flask

from controllers.routes import routes


app = Flask(
    __name__,
    template_folder="views",
    static_folder="static"
)


app.register_blueprint(routes)


if __name__ == "__main__":

    app.run(
        debug=True
    )