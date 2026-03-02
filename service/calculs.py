from service import db_manager
import pandas as pd
from fpdf import FPDF

def calcul_total_encaisse():
    encaissements = db_manager.get_all_encaissements()
    total = 0

    for e in encaissements:
        montant = e[3]  # index du montant
        total += montant

    return total


def calcul_total_depenses():
    depenses = db_manager.get_all_depenses()
    total = 0

    for d in depenses:
        montant = d[3]  # index du montant
        total += montant

    return total


def calcul_solde():
    total_encaisse = calcul_total_encaisse()
    total_depenses = calcul_total_depenses()
    solde = total_encaisse - total_depenses
    return solde


def calcul_montant_paye_par_donateur(donateur_id):
    encaissements = db_manager.get_encaissements_by_donateur(donateur_id)
    total = 0

    for e in encaissements:
        total += e[0]

    return total


def calcul_reste_a_payer(donateur_id):
    donateurs = db_manager.get_all_donateurs()

    montant_promis = 0
    for d in donateurs:
        if d[0] == donateur_id:  # id_donateur
            montant_promis = d[2]  # montant_promis
            break

    montant_paye = calcul_montant_paye_par_donateur(donateur_id)
    if montant_promis != 0:
        reste = montant_promis - montant_paye
    else:
        reste = 0
    return reste


def calcul_statut_donateur(donateur_id):
    donateurs = db_manager.get_all_donateurs()

    montant_promis = 0
    for d in donateurs:
        if d[0] == donateur_id:
            montant_promis = d[2]
            break

    montant_paye = calcul_montant_paye_par_donateur(donateur_id)
    if montant_promis == 0:
        return "Payé"

    if montant_paye >= montant_promis and montant_promis > 0:
        return "Payé"
    elif montant_paye > 0 and montant_paye < montant_promis:
        return "Partiel"
    else:
        return "Non payé"


def get_statut_tous_donateurs():
    donateurs = db_manager.get_all_donateurs()
    resultat = []

    for d in donateurs:
        donateur_id = d[0]
        nom = d[1]
        montant_promis = d[2]

        
        montant_paye = calcul_montant_paye_par_donateur(donateur_id)
        if montant_promis != 0:
            reste = montant_promis - montant_paye
        else:
            reste = 0
        statut = calcul_statut_donateur(donateur_id)

        resultat.append({
            "nom": nom,
            "montant_promis": montant_promis,
            "montant_paye": montant_paye,
            "reste_a_payer": reste,
            "statut": statut
        })

    return resultat




def calcul_encaissements_par_jour(date):
    encaissements = db_manager.get_all_encaissements()
    total = 0
    liste = []

    for e in encaissements:
        # e = (id_encaissement, nom, date, montant, remarque)
        if e[2] == date:
            total += e[3]
            liste.append(e)

    return total, liste


def calcul_depenses_par_jour(date):
    depenses = db_manager.get_all_depenses()
    total = 0
    liste = []

    for d in depenses:
        # d = (id_depense, date, motif, montant)
        if d[1] == date:
            total += d[3]
            liste.append(d)

    return total, liste


def rapport_journalier(date):
    total_encaisse, liste_encaissements = calcul_encaissements_par_jour(date)
    total_depenses, liste_depenses = calcul_depenses_par_jour(date)

    solde = total_encaisse - total_depenses

    return {
        "total_encaisse": total_encaisse,
        "total_depenses": total_depenses,
        "solde": solde,
        "encaissements": liste_encaissements,
        "depenses": liste_depenses
    }



def calcul_encaissements_par_mois(annee, mois):
    encaissements = db_manager.get_all_encaissements()
    total = 0
    liste = []

    for e in encaissements:
        # e[2] = date (YYYY-MM-DD)
        date = e[2]
        an = date[:4]
        m = date[5:7]

        if an == str(annee) and m == f"{mois:02d}":
            total += e[3]
            liste.append(e)

    return total, liste


def calcul_depenses_par_mois(annee, mois):
    depenses = db_manager.get_all_depenses()
    total = 0
    liste = []

    for d in depenses:
        # d[1] = date
        date = d[1]
        an = date[:4]
        m = date[5:7]

        if an == str(annee) and m == f"{mois:02d}":
            total += d[3]
            liste.append(d)

    return total, liste


def rapport_mensuel(annee, mois):
    total_encaisse, liste_encaissements = calcul_encaissements_par_mois(annee, mois)
    total_depenses, liste_depenses = calcul_depenses_par_mois(annee, mois)

    solde = total_encaisse - total_depenses

    return {
        "total_encaisse": total_encaisse,
        "total_depenses": total_depenses,
        "solde": solde,
        "encaissements": liste_encaissements,
        "depenses": liste_depenses
    }



def calcul_annuel(annee):
    encaissements = db_manager.get_all_encaissements()
    depenses = db_manager.get_all_depenses()

    totaux_encaissements = [0] * 12
    totaux_depenses = [0] * 12

    # Encaissements
    for e in encaissements:
        date = e[2]  # YYYY-MM-DD
        an = int(date[:4])
        mois = int(date[5:7])

        if an == annee:
            totaux_encaissements[mois - 1] += e[3]

    # Dépenses
    for d in depenses:
        date = d[1]
        an = int(date[:4])
        mois = int(date[5:7])

        if an == annee:
            totaux_depenses[mois - 1] += d[3]

    soldes = []
    for i in range(12):
        soldes.append(totaux_encaissements[i] - totaux_depenses[i])

    return totaux_encaissements, totaux_depenses, soldes





















def export_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename



def export_pdf(titre, data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    pdf.cell(200, 10, txt=titre, ln=True, align="C")

    if isinstance(data, list):
        for row in data:
            pdf.multi_cell(0, 8, txt=str(row))
    else:
        for key, value in data.items():
            pdf.cell(0, 8, txt=f"{key} : {value}", ln=True)

    pdf.output(filename)
    return filename