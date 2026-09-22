from flask import Flask,jsonify,request
import mysql.connector
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)

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