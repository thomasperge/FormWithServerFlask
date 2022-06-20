# Import:
import sqlite3

# ============> ADHERENT <============
# Ajout Adherent:
def add_adh(nom, prenom, age, username):
    """
    Ajouter un Adherent selon: le Nom, le Prenom, l'Age et son Username
    (le username est unique, il ne peut pas y avoir deux identique)
    """
    conn = sqlite3.connect('DataBase.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO adherent (nom, prenom, age, username) VALUES (\"%s\", \"%s\", \"%i\", \"%s\") """%(nom, prenom, age, username))
    conn.commit()
    return True

# Suppresion Adherent:
def suppr_adh(username):
    """
    Surprime un adherent de la base de donnée selon son Username
    """
    conn = sqlite3.connect('DataBase.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM adherent WHERE username = (\"%s\") """%(username))
    conn.commit()


# ============> PARTICIPANT <============
# Ajout Participant:
def add_participation(username, lieu):
    """
    La fonction recupère le Username de l'Adherent et le Lieu de la rencontre.
    En fonction de ces 2 critères, on cherche l'identifiant de l'Adherent grâce au username et
    l'identifiant correspondant à la rencontre.
    On ajoute à la table participation:l'identifiant de l'utilisateur, et, l'identifiant de la rencontre.
    """
    conn = sqlite3.connect('DataBase.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # == Recupère le Username (identifiant) ==
    req = """
    SELECT id, username FROM adherent
    WHERE adherent.username = (\"%s\")
        """%(username)

    result = cursor.execute(req)
    for raw2 in result:
        id_username = raw2[0]

    # == Recupère le lieu (identifiant) ==
    req2 = """
    SELECT id_rencontre, lieu FROM rencontre
    WHERE rencontre.lieu = (\"%s\")
    """%(lieu)

    result2 = cursor.execute(req2)
    for raw2 in result2:
        id_rencontre = raw2[0]

    # == Condition: Si il a 10 joueurs déjà enregistré ==
    log = """
    SELECT COUNT(id_rencontre) AS nbParticipation FROM participation
    WHERE participation.id_rencontre = (\"%i\")
    """%(id_rencontre)

    result3 = cursor.execute(log)
    for raw in result3:
        # == si il y a + de 10 Joueurs: ==
        if raw[0] >= 10:
            print('Error, trop de joueur, max 10...')
            return False
        # == si il y a - de 10 joueurs: ==
        else:
            req3 = """
            INSERT INTO participation
            VALUES((\"%s\"), (\"%s\"))
            """%(id_username, id_rencontre)
            
            cursor.execute(req3)
            conn.commit()

# Supression Participant:
def suppr_participation(username, lieu):
    """
    La fonction recupère le Username de l'Adherent et le Lieu de la rencontre.
    En fonction de ces 2 critères, on cherche l'identifiant de l'Adherent grâce au username et
    l'identifiant correspondant à la rencontre grâce au lieu donné préalablement en paramètre.
    On supprime definitivement les identifiants (id_participant, id_rencontre) à la table participation.
    """
    conn = sqlite3.connect('DataBase.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # == Recupère le Username (identifiant) ==
    req = """
    SELECT id, username FROM adherent
    WHERE adherent.username = (\"%s\")
        """%(username)

    result = cursor.execute(req)
    for raw2 in result:
        id_username = raw2[0]

    # == Recupère le lieu (identifiant) ==
    req2 = """
    SELECT id_rencontre, lieu FROM rencontre
    WHERE rencontre.lieu = (\"%s\")
    """%(lieu)

    result2 = cursor.execute(req2)
    for raw2 in result2:
        id_rencontre = raw2[0]

    # == Effacer les données ==
    cursor.execute("""DELETE FROM participation WHERE id_participant = (\"%i\") AND id_rencontre = (\"%i\");"""%(id_username, id_rencontre))
    conn.commit()

# Affiche la participation de tout les adherents:
def participant(rencontre_lieu, rencontre_date):
    """
    Avec comme parametre le lieu et la date de la rencontre, renvoye le(s)
    participant(s) de cette rencontre selon la table participation
    """
    conn = sqlite3.connect('DataBase.db', check_same_thread=False)
    cursor = conn.cursor()
    req = """
    SELECT * FROM participation JOIN rencontre JOIN adherent
    ON participation.id_rencontre = rencontre.id_rencontre
    AND participation.id_participant = adherent.id
    WHERE rencontre.lieu = (\"%s\") AND rencontre.date = (\"%s\")
        """%(rencontre_lieu, rencontre_date)
    
    result = cursor.execute(req)
    for raw in result:
        print(raw)
    conn.commit()

# ============> RENCONTRE <============
# Ajout Rencontre:
def add_rencontre(lieu, date, id_responsable):
    """
    Permet l'ajout d'une Rencontre dans la base de Donnée selon: le Lieu, la Date, et le Responsable
    """
    conn = sqlite3.connect('DataBase.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO rencontre(lieu, date, id_responsable) VALUES(\"%s\", \"%s\", \"%i\");"""%(lieu, date, id_responsable))
    conn.commit()

# Supression Rencontre:
def suppr_rencontre(lieu):
    """
    Permet la supression d'une Participation dans la base de Donnée
    """
    conn = sqlite3.connect('DataBase.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM rencontre WHERE lieu = (\"%s\")"""%(lieu))
    conn.commit()



# =====================================
# Appel des Fonctions pour voir leurs fonctionnement: (attention: changer les valeurs, car certaine sont déjà enregistrée!)
def appelFunction():
    add_adh('Test2', 'Test2', 22, 'TestUsername')
    suppr_adh('TestUsername')
    add_participation('TestUsername', 'Texas')
    suppr_participation('TestUsername', 'Texas')
    participant('Silicon Valley', '25/12/2021')
    add_rencontre('Los Angeles', '25/12/2023', 4)
    suppr_rencontre('Los Angeles')


if __name__ == '__main__':
    appelFunction()