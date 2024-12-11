from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re
import logging

app = Flask(__name__)

# Configurer la base de données
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'adelbbc'
app.config['MYSQL_DB'] = 'ADVAN_QUIZ'

mysql = MySQL(app)

# Endpoint pour l'inscription
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Tous les champs sont requis"}), 400

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return jsonify({"error": "Email invalide"}), 400

    if len(password) < 8:
        return jsonify({"error": "Le mot de passe doit contenir au moins 8 caractères"}), 400

    hashed_password = generate_password_hash(password)

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, hashed_password))
        mysql.connection.commit()
        return jsonify({"message": "Utilisateur créé avec succès"}), 201
    except Exception as e:
        logging.error(f"Erreur lors de l'inscription : {e}")
        return jsonify({"error": "Email ou nom d'utilisateur déjà utilisé"}), 400
    finally:
        cur.close()

# Endpoint pour la connexion
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email_or_username = data.get('emailOrUsername')  # Champ unique pour email ou nom d'utilisateur
    password = data.get('password')

    cur = mysql.connection.cursor()
    try:
        query = """
            SELECT password_hash FROM users 
            WHERE email = %s OR username = %s
        """
        cur.execute(query, (email_or_username, email_or_username))
        user = cur.fetchone()
    finally:
        cur.close()

    if user and check_password_hash(user[0], password):
        return jsonify({"message": "Connexion réussie"}), 200
    else:
        return jsonify({"error": "Identifiants incorrects"}), 401

@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * FROM quizzes")
        quizzes = cur.fetchall()
        return jsonify({"quizzes": quizzes}), 200
    finally:
        cur.close()

