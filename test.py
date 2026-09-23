from flask import Flask,jsonify,request,session,send_from_directory
import mysql.connector
app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def home():
    return send_from_directory(".", "index.html")

@app.route("/employe.html")
def page_employe():
    return send_from_directory(".", "employe.html")

def get_connexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1234", 
        database="water_management"
    )

@app.route("/api/demandes")
def get_demandes():
    conn = get_connexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM demandes")
    resultat = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultat)



from flask import request

@app.route("/api/demandes", methods=["POST"])
def add_demande():
    data = request.get_json()
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO demandes (objet, statut) VALUES (%s, %s)",
        (data["objet"], "en cours")
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Demande ajoutée avec succès"}), 201
from flask import session

app.secret_key = "une_cle_secrete_123"  # nécessaire pour les sessions

# Compte employé simple (en dur pour l'instant)
EMPLOYE = {"username": "employe1", "password": "azerty123"}

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if data["username"] == EMPLOYE["username"] and data["password"] == EMPLOYE["password"]:
        session["connecte"] = True
        return jsonify({"message": "Connexion réussie"})
    return jsonify({"message": "Identifiants incorrects"}), 401

@app.route("/api/statut", methods=["GET"])
def check_login():
    return jsonify({"connecte": session.get("connecte", False)})

if __name__ == "__main__":
    app.run(debug=True)