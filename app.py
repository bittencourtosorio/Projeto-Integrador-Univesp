from flask import Flask, render_template, jsonify, request
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import os, datetime
from werkzeug.exceptions import abort
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import pymysql

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "base_conhecimento_db.db"))

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'localhost',
    'user': 'roots',
    'password': '',
    'database': 'base_conhecimento_db'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SECRET_KEY'] = 'YOUR SECRET KEY HERE'
db = SQLAlchemy(app)

class Maquinas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maquina = db.Column(db.String(20), nullable=False)

@app.route("/")

def index():
    maquinas = Maquinas.query.all()
    return render_template("base de conhecimento.html", maquinas=maquinas)


@app.route('/api/maquinas', methods=['GET'])
def get_maquinas():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT maquina FROM maquinas ORDER BY maquina")
        maquinas = cursor.fetchall()
        return jsonify(maquinas)
    except Error as e:
        print(f"Erro ao buscar máquinas: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route('/api/defeitos', methods=['GET', 'POST'])
def defeitos():
    if request.method == 'GET':
        # Implementar busca de defeitos se necessário
        pass
    elif request.method == 'POST':
        data = request.get_json()

        # Validação básica
        if not all(key in data for key in ['maquina', 'defeito', 'solucao']):
            return jsonify({'error': 'Dados incompletos'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

        try:
            cursor = conn.cursor()
            query = """
                    INSERT INTO defeitos_registrados
                        (maquina, defeito, solucao, causa, data_registro)
                    VALUES (%s, %s, %s, %s, NOW()) \
                    """
            cursor.execute(query, (
                data['maquina'],
                data['defeito'],
                data['solucao'],
                data.get('causa', '')
            ))
            conn.commit()
            return jsonify({'success': True}), 201
        except Error as e:
            conn.rollback()
            print(f"Erro ao registrar defeito: {e}")
            return jsonify({'error': str(e)}), 500
        finally:
            if conn.is_connected():
                conn.close()


if __name__ == '__main__':
    app.run(debug=True)
