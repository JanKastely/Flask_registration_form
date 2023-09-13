import os
from flask_talisman import Talisman
from flask import Flask, request, redirect, url_for



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev',DATABASE=os.path.join(app.instance_path, 'register.sqlite'),)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    Talisman(app, content_security_policy="default-src 'self'")



    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    from register import db
    db.init_app(app)

    from register import auth
    app.register_blueprint(auth.bp)

    from register import security_headers

    from register import forms

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
