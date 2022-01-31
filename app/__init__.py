# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from .backend.model import create_model

classes = {0: "Livres et romans",
           1: "Magazines",
           2: "Accessoires jeux videos",
           3: "Jouets enfance",
           4: "Livres et illustres",
           5: "Papeteries",
           6: "Mobiliers jardin et cuisine",
           7: "Mobiliers intérieurs et litteries",
           8: "Jeux de société",
           9: "Accessoires intérieurs",
           10: "Livres jeunesse",
           11: "Goodies geek",
           12: "Piscine spa",
           13: "Figurines Wargames",
           14: "Modèles réduits ou télécommandes",
           15: "Jeux geek",
           16: "Cartes de collection",
           17: "Décoration Intérieur",
           18: "Jeux videos",
           19: "Jeux et consoles retro",
           20: "Petite enfance",
           21: "Jouets enfants",
           22: "Accessoires animaux",
           23: "Jeux videos dematerialises",
           24: "Jardin et bricolage",
           25: "Epicerie",
           26: "Matériel enfance"}

db = SQLAlchemy()
model = create_model()


def init_app():
    """Construct the core application."""
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

        return app
