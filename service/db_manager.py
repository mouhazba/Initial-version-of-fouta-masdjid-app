import sqlite3
from pathlib import Path

DB_PATH = Path("database/database.db")

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table Donateurs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donateurs (
        id_donateur INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        montant_promis REAL DEFAULT 0,
        date_promesse TEXT
    )
    """)

    # Table Encaissements
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS encaissements (
        id_encaissement INTEGER PRIMARY KEY AUTOINCREMENT,
        donateur_id INTEGER,
        date TEXT NOT NULL,
        montant REAL NOT NULL,
        remarque TEXT,
        FOREIGN KEY (donateur_id) REFERENCES donateurs(id_donateur)
    )
    """)

    # Table Depenses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS depenses (
        id_depense INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        motif TEXT NOT NULL,
        montant REAL NOT NULL
    )
    """)


    conn.commit()
    conn.close()

# ******************************************** Fonctions pour les donateurs ********************************************
def get_all_donateurs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donateurs")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_donateur(nom, montant_promis, date_promesse):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO donateurs (nom, montant_promis, date_promesse)
        VALUES (?, ?, ?)
    """, (nom, montant_promis, date_promesse))
    conn.commit()
    conn.close()


def get_donateur_by_id(donateur_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donateurs WHERE id_donateur = ?", (donateur_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_donateur(donateur_id, nom, montant_promis, date_promesse):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE donateurs
        SET nom = ?, montant_promis = ?, date_promesse = ?
        WHERE id_donateur = ?
    """, (nom, montant_promis, date_promesse, donateur_id))
    conn.commit()
    conn.close()


def delete_donateur(donateur_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # (option sécurité) supprimer d’abord ses encaissements
    cursor.execute("DELETE FROM encaissements WHERE donateur_id = ?", (donateur_id,))
    cursor.execute("DELETE FROM donateurs WHERE id_donateur = ?", (donateur_id,))

    conn.commit()
    conn.close()
# ******************************************** Fonctions pour les encaissements ********************************************


def get_all_encaissements():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT encaissements.id_encaissement,
               donateurs.nom,
               encaissements.date,
               encaissements.montant,
               encaissements.remarque
        FROM encaissements
        LEFT JOIN donateurs ON encaissements.donateur_id = donateurs.id_donateur
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_encaissements_by_donateur(donateur_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT montant FROM encaissements
        WHERE donateur_id = ?
    """, (donateur_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_encaissement(donateur_id, date_encaissement, montant, remarque):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO encaissements (donateur_id, date, montant, remarque)
        VALUES (?, ?, ?, ?)
    """, (donateur_id, date_encaissement, montant, remarque))
    conn.commit()
    conn.close()

def get_donateurs_for_select():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id_donateur, nom FROM donateurs")
    rows = cursor.fetchall()
    conn.close()
    return rows



def get_encaissement_by_id(encaissement_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_encaissement, donateur_id, date, montant, remarque
        FROM encaissements
        WHERE id_encaissement = ?
    """, (encaissement_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_encaissement(encaissement_id, donateur_id, date_encaissement, montant, remarque):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE encaissements
        SET donateur_id = ?, date = ?, montant = ?, remarque = ?
        WHERE id_encaissement = ?
    """, (donateur_id, date_encaissement, montant, remarque, encaissement_id))
    conn.commit()
    conn.close()
# ******************************************** Fonctions pour les dépenses ********************************************
def add_depense(date_depense, motif, montant):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO depenses (date, motif, montant)
        VALUES (?, ?, ?)
    """, (date_depense, motif, montant))
    conn.commit()
    conn.close()


def get_all_depenses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM depenses")
    rows = cursor.fetchall()
    conn.close()
    return rows


# Suppression de toutes les lignes (ou certaines lignes)
def delete_all_depenses_and_reset_id():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Supprimer toutes les encaissements
    cur.execute("DELETE FROM encaissements")

    # Réinitialiser l'AUTOINCREMENT
    cur.execute("DELETE FROM sqlite_sequence WHERE name='encaissements'")

def get_depense_by_id(depense_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_depense, date, motif, montant
        FROM depenses
        WHERE id_depense = ?
    """, (depense_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_depense(depense_id, date_depense, motif, montant):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE depenses
        SET date = ?, motif = ?, montant = ?
        WHERE id_depense = ?
    """, (date_depense, motif, montant, depense_id))
    conn.commit()
    conn.close()


def delete_depense(depense_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM depenses WHERE id_depense = ?", (depense_id,))
    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_tables()
    print("Base de données et tables créées avec succès.")
    delete_all_depenses_and_reset_id()
    delete_depense(29)
    
    
    
    
    
    
    
    
    
    
    
    
    
#delete_all_depenses_and_reset_id()