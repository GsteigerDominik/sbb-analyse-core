from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
    )

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app