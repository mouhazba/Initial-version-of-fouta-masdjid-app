#from altair.theme import get
import streamlit as st
from service.db_manager import add_depense, get_all_depenses, get_depense_by_id, get_donateurs_for_select, update_depense
import pandas as pd
from datetime import date


# ======================
# authenticated
# ======================
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("⛔ Accès refusé. Veuillez vous connecter.")
    st.stop()

st.title("📊 Ramadan de Fouta Masdjid ")

# =========================
# LISTE DES DÉPENSES
# =========================
st.title("Dépenses")

st.subheader("Liste des dépenses")

depenses = get_all_depenses()

if depenses:
    col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 2, 1])
    col1.markdown("**ID**")
    col2.markdown("**Date**")
    col3.markdown("**Motif**")
    col4.markdown("**Montant**")
    col5.markdown("**Action**")

    for d in depenses:
        # d = (id_depense, date, motif, montant)
        col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 2, 1])

        col1.write(d[0])
        col2.write(d[1])
        col3.write(d[2])
        col4.write(d[3])

        if col5.button("✏️", key=f"edit_dep_{d[0]}"):
            st.session_state["edit_depense_id"] = d[0]

else:
    st.info("Aucune dépense enregistrée.")

st.divider()

# =========================
# FORMULAIRE MODIFICATION
# =========================
if "edit_depense_id" in st.session_state:
    dep = get_depense_by_id(st.session_state["edit_depense_id"])

    st.subheader("✏️ Modifier la dépense")

    with st.form("form_edit_depense"):
        date_edit = st.date_input("Date", value=pd.to_datetime(dep[1]))
        motif_edit = st.text_input("Motif", value=dep[2])
        montant_edit = st.number_input("Montant", min_value=0.0, value=float(dep[3]))

        submit_edit = st.form_submit_button("💾 Sauvegarder")

    if submit_edit:
        update_depense(
            dep[0],
            str(date_edit),
            motif_edit,
            montant_edit
        )

        st.success("Dépense modifiée avec succès !")
        del st.session_state["edit_depense_id"]
        st.rerun()

st.divider()
# =========================
# FORMULAIRE AJOUT
# =========================
st.subheader("Ajouter une dépense")

with st.form("form_depense"):
    date_depense = st.date_input("Date", value=date.today())
    motif = st.text_input("Motif de la dépense")
    montant = st.number_input("Montant dépensé", min_value=0.0)
    submit = st.form_submit_button("Enregistrer")

if submit:
    if motif.strip() == "":
        st.error("Le motif est obligatoire.")
    elif montant <= 0:
        st.error("Le montant doit être supérieur à 0.")
    else:
        add_depense(str(date_depense), motif, montant)
        st.success("Dépense enregistrée avec succès !")
        st.rerun()



