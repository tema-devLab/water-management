from flask import Flask,jsonify
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