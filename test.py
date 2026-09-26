from flask import Flask,jsonify,request,session,send_from_directory
import mysql.connector
import uuid
app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def home():
    return send_from_directory(".", "index.html")

@app.route("/employe.html")
def page_employe():
    if not session.get("connecte"):
        return "<h2>Accès refusé — veuillez vous connecter d'abord.</h2><a href='/index.html'>Retour à la connexion</a>", 401
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
    if not session.get("citoyen_id"):
        return jsonify({"message": "Veuillez créer un compte ou vous connecter"}), 401
    data = request.get_json()
    numero = "DEM-" + str(uuid.uuid4())[:8].upper()
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO demandes (objet, type_demande, statut, numero_suivi, citoyen_id) VALUES (%s, %s, %s, %s, %s)",
        (data["objet"], data["type_demande"], "en cours", numero, session["citoyen_id"])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Demande ajoutée", "numero_suivi": numero}), 201
@app.route("/api/suivi/<numero>")
def suivre_demande(numero):
    conn = get_connexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT statut FROM demandes WHERE numero_suivi = %s", (numero,))
    resultat = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultat:
        return jsonify(resultat)
    return jsonify({"message": "Numéro introuvable"}), 404

from flask import session
app.secret_key = "une_cle_secrete_123"  
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    conn = get_connexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM employes WHERE username = %s AND password = %s",
        (data["username"], data["password"])
    )
    employe = cursor.fetchone()
    cursor.close()
    conn.close()
    if employe:
        session["connecte"] = True
        session["nom"] = employe["nom"]
        return jsonify({"message": "Connexion réussie", "nom": employe["nom"]})
    return jsonify({"message": "Identifiants incorrects"}), 401

@app.route("/api/statut", methods=["GET"])
def check_login():
    return jsonify({"connecte": session.get("connecte", False)})

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Déconnecté"})

@app.route("/api/citoyen/inscription", methods=["POST"])
def inscription_citoyen():
    data = request.get_json()
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO citoyens (nom, prenom, username, password) VALUES (%s, %s, %s, %s)",
        (data["nom"], data["prenom"], data["username"], data["password"])
    )
    conn.commit()
    citoyen_id = cursor.lastrowid
    cursor.close()
    conn.close()
    session["citoyen_id"] = citoyen_id
    return jsonify({"message": "Compte créé", "citoyen_id": citoyen_id}), 201

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")