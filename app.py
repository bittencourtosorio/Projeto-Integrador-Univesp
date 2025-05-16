from flask import Flask, render_template
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import os, datetime

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "base_conhecimento_db.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SECRET_KEY'] = 'YOUR SECRET KEY HERE'
db = SQLAlchemy(app)

class Maquinas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maquina = db.Column(db.String(20), nullable=False)

@app.route("/")

def index():
    return render_template("index.html")

