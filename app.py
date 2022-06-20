# -----------------------------
# - Imports:
from flask import Flask, render_template, request
import sqlite3
from main import add_adh as ajout_adherent, suppr_adh as supprimer_adherent, add_participation as ajoutParticipation, suppr_participation as supprimer_participation, add_rencontre as ajouter_rencontre, suppr_rencontre as supprimer_rencontre

# -----------------------------
# - Setup:
app = Flask(__name__)

# -----------------------------
# - Routes:

# ==== Main ====
@app.route('/')
def main_welcome():
    return render_template("index.html")

@app.route('/index.html')
def index():
    return render_template("index.html")
# ==============


# ===================== (Adherent Part) ======================
# ==== Ajout Adherent ====
@app.route('/addAdh.html', methods=['GET', 'POST'])
def addAdh():
    if request.method == 'POST':
        # --- HTML Form ---
        username = request.form['username'] 
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = request.form['age']
        # --- Query ---
        if username == '' or nom == '' or prenom == '' or age == '':
            return render_template("error.html")
        else:
            ajout_adherent(nom, prenom, int(age), username)
    return render_template("addAdh.html")
# ========================

# ==== Delete Adherent ====
@app.route('/supprAdh.html', methods=['GET', 'POST'])
def supprAdh():
    if request.method == 'POST':
        # --- HTML Form ---
        username_user = request.form['username_adh']
        # --- Query ---
        if username_user == '':
            return render_template("error.html")
        else:
            supprimer_adherent(username_user)
    return render_template("supprAdh.html")
# =========================

# ==== Display Adherent ====
@app.route('/allAdh.html')
def allAdherent():
    # --- Query ---
    connection = sqlite3.connect("DataBase.db", check_same_thread=False)
    cursor = connection.cursor()
    fas = cursor.execute('SELECT * FROM adherent')
    return render_template('allAdh.html', items=fas.fetchall())
# ==========================

# Fin Adherent Part:
# =========================================================




# ===================== (Participation Part) =====================
# ==== Ajout Participation ====
@app.route('/addParticipation.html', methods=['GET', 'POST'])
def addParticipation():
    print('here')
    # --- HTML Form ---
    username = request.form.get('username_adherent_part')
    lieu = request.form.get('lieu_rencontre_part')
    # --- Query ---
    if lieu == '' or username == '':
        return render_template("error.html")
    else:
        if username != None or lieu != None:
            ajoutParticipation(username, lieu)    
    return render_template("addParticipation.html")
# =============================

# ==== Supression Participation ====
@app.route('/supprParticipation.html', methods=['GET', 'POST'])
def supprParticipant():
    if request.method == 'POST':
        # --- HTML Form ---
        username = request.form['username_suppr']
        lieu = request.form['lieu_suppr']
        # --- Query ---
        if username == '' or lieu == '':
            return render_template("error.html")
        else:
            supprimer_participation(username, lieu)
    return render_template("supprParticipation.html")
# ==================================


# ==== Display Participation ====
@app.route('/allParticipant.html', methods=['GET', 'POST'])
def allParticipant():
    # --- HTML Form ---
    connection = sqlite3.connect("DataBase.db", check_same_thread=False)
    cursor = connection.cursor()
    rencontre_lieu = request.form.get('rencontre_lieu')
    rencontre_date = request.form.get('rencontre_date')
    # --- Query ---
    if rencontre_lieu == '' or rencontre_date == '':
        return render_template("error.html")
    else:
        fas = cursor.execute("""
        SELECT * FROM participation JOIN rencontre JOIN adherent
        ON participation.id_rencontre = rencontre.id_rencontre
        AND participation.id_participant = adherent.id 
        WHERE rencontre.lieu = (\"%s\") AND rencontre.date = (\"%s\")
        """%(rencontre_lieu, rencontre_date))
    return render_template('allParticipant.html', items=fas.fetchall(), lieu_renc=rencontre_lieu, date_renc= rencontre_date)
# ===============================

# Fin Participant Part:
# =================================================================




# ===================== (Rencontre Part) =====================
# ==== Ajouter Rencontre ====
@app.route('/addRencontre.html', methods=['GET', 'POST'])
def addRencontre():
    if request.method == 'POST':
        # --- HTML Form ---
        lieu = request.form['lieu_rencontre']
        date = request.form['date_rencontre']
        id_respons = request.form['idRespons_rencontre']
        # --- Query ---
        if lieu == '' or date == ''or id_respons == '':
            return render_template("error.html")
        else:
            ajouter_rencontre(lieu, date, int(id_respons))
    return render_template("addRencontre.html")
# ===========================

# ==== Supprimer Rencontre ====
@app.route('/supprRencontre.html', methods=['GET', 'POST'])
def supprRencontre():
    if request.method == 'POST':
        # --- HTML Form ---
        lieu_rencontre = request.form['lieu_rencontre']
        # --- Query ---
        if lieu_rencontre == '':
            return render_template("error.html")
        else:
            supprimer_rencontre(lieu_rencontre)
    return render_template("supprRencontre.html")
# =============================

# ==== Display Rencontre ====
@app.route('/allRencontre.html')
def allRencontre():
    # --- Query ---
    connection = sqlite3.connect("DataBase.db", check_same_thread=False)
    cursor = connection.cursor()
    fas = cursor.execute('SELECT * FROM rencontre')
    return render_template('allRencontre.html', items=fas.fetchall())
# ===========================

# Fin Rencontre Part:
# ============================================================



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)