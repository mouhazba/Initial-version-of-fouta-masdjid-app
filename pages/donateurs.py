import streamlit as st
import pandas as pd
from datetime import date
from service.db_manager import (
    get_all_donateurs,
    add_donateur,
    update_donateur,
    delete_donateur
)


# ======================
# authenticated
# ======================
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("⛔ Accès refusé. Veuillez vous connecter.")
    st.stop()

st.title("📊 Ramadan de Fouta Masdjid ")
st.title("Donateurs")

# =========================
# LISTE DES DONATEURS
# =========================
st.subheader("Liste des donateurs")

donateurs = get_all_donateurs()

if donateurs:
    df = pd.DataFrame(donateurs, columns=["ID", "Nom", "Montant Promis", "Date Promesse"])
    col1, col2, col3, col4, col5 = st.columns([ 1, 3, 2, 2, 2])
    col1.markdown("**ID**")
    col2.markdown("**Nom**")
    col3.markdown("**Montant Promis**")
    col4.markdown("**Date Promesse**")
    col5.markdown("**Actions**")
    for d in donateurs:
        col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 2, 1, 1])

        col1.write(d[0])
        col2.write(d[1])
        col3.write(d[2])
        col4.write(d[3])

        if col5.button("✏️", key=f"edit_{d[0]}"):
            st.session_state["edit_id"] = d[0]

        if col6.button("🗑️", key=f"delete_{d[0]}"):
            st.session_state["delete_id"] = d[0]

else:
    st.info("Aucun donateur enregistré.")

st.divider()
# =========================
# CONFIRMATION SUPPRESSION
# =========================
if "delete_id" in st.session_state:
    donateur = [d for d in donateurs if d[0] == st.session_state["delete_id"]][0]

    st.warning(f"⚠️ Voulez-vous vraiment supprimer le donateur : {donateur[1]} ?")

    col1, col2 = st.columns(2)

    if col1.button("✅ Oui, supprimer"):
        delete_donateur(donateur[0])
        st.success("Donateur supprimé avec succès !")
        del st.session_state["delete_id"]
        st.rerun()

    if col2.button("❌ Annuler"):
        del st.session_state["delete_id"]
        st.info("Suppression annulée.")
        st.rerun()

# =========================
# FORMULAIRE DE MODIFICATION
# =========================
if "edit_id" in st.session_state:
    donateur = [d for d in donateurs if d[0] == st.session_state["edit_id"]][0]

    st.subheader("✏️ Modifier le donateur")

    with st.form("form_edit_donateur"):
        nom_edit = st.text_input("Nom", value=donateur[1])
        montant_edit = st.number_input("Montant promis", min_value=0.0, value=float(donateur[2]))
        date_edit = st.date_input("Date promesse", value=pd.to_datetime(donateur[3]))

        submit_edit = st.form_submit_button("💾 Sauvegarder")

    if submit_edit:
        update_donateur(donateur[0], nom_edit, montant_edit, str(date_edit))
        st.success("Donateur modifié avec succès !")
        st.session_state.pop("edit_id", None)  # SUPPRESSION propre
        st.rerun()
st.divider()

# =========================
# FORMULAIRE AJOUT DONATEUR
# =========================
st.subheader("Ajouter un donateur")

with st.form("form_donateur"):
    nom = st.text_input("Nom du donateur")
    montant_promis = st.number_input("Montant promis (0 si aucun)", min_value=0.0)
    date_promesse = st.date_input("Date de la promesse", value=date.today())
    submit = st.form_submit_button("Enregistrer")

if submit:
    if nom.strip() == "":
        st.error("Le nom est obligatoire.")
    else:
        add_donateur(nom, montant_promis, str(date_promesse))
        st.success("Donateur ajouté avec succès !")
        st.rerun()