from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re
import logging

# Configure les logs pour Flask
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)
    print(app.url_map)



# Configurer la base de données
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'adelbbc'
app.config['MYSQL_DB'] = 'ADVAN_QUIZ'

mysql = MySQL(app)




@app.route('/', methods=['GET'])
def home():
    print("La route / a été atteinte")
    return render_template('index.html')  # Nom du fichier HTML dans le dossier 'templates'


@app.route('/create-account', methods=['GET'])
def create_account():
    return render_template('create-account.html')  # Page de destination


@app.route('/connexion')
def connexion():
    return render_template('connexion.html')



@app.route('/inscription')
def inscription():
    return render_template('inscription.html')  # Charge la page d'inscription


@app.route('/theme')
def theme():
    return render_template('quiz-section.html')  # Charge la page d'inscription




@app.route('/register', methods=['POST'])
def register():
    print("En-têtes de la requête :", request.headers)
    print("Données brutes :", request.data.decode('utf-8'))  # Decode les bytes en string

    if not request.is_json:
        return jsonify({"error": "Le contenu doit être au format JSON"}), 415

    try:
        data = request.get_json()
        print("Données JSON :", data)
    except Exception as e:
        return jsonify({"error": "Erreur de parsing JSON"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    print("Données extraites : username=", username, " email=", email, " password=", password)

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






@app.route('/leaderboard/<theme>', methods=['GET'])
def leaderboard(theme):
    cur = mysql.connection.cursor()
    try:
        query = """
        SELECT users.username, scores.score, scores.created_at
        FROM scores
        JOIN users ON scores.user_id = users.id
        JOIN themes ON scores.theme_id = themes.id
        WHERE themes.name = %s
        ORDER BY scores.score DESC
        LIMIT 10
        """
        cur.execute(query, (theme,))
        leaderboard = cur.fetchall()
        return jsonify({"leaderboard": leaderboard}), 200
    finally:
        cur.close()





@app.route('/get-questions/<theme>', methods=['GET'])
def get_questions(theme):
    cur = mysql.connection.cursor()
    try:
        query = """
        SELECT question_text, option_a, option_b, option_c, option_d, correct_option, points
        FROM questions
        JOIN themes ON questions.theme_id = themes.id
        WHERE themes.name = %s
        """
        cur.execute(query, (theme,))
        questions = cur.fetchall()
        return jsonify({"questions": questions}), 200
    finally:
        cur.close()

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.json
    question_id = data.get('question_id')
    answer = data.get('answer')

    cur = mysql.connection.cursor()
    try:
        query = "SELECT correct_option FROM questions WHERE id = %s"
        cur.execute(query, (question_id,))
        correct_option = cur.fetchone()[0]
        is_correct = (answer == correct_option)
        return jsonify({"is_correct": is_correct}), 200
    finally:
        cur.close()






