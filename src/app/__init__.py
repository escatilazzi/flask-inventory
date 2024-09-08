import os
from flask import Flask, render_template
from .models import db
from .routes import auth_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Nueva123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/flask_psychology'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(auth_blueprint)
    
    @app.route('/')
    def home():
        return render_template('home.html')

    return app