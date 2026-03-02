import streamlit as st
import pandas as pd
from datetime import date

from service.db_manager import (
    get_all_encaissements,
    get_donateurs_for_select,
    add_encaissement,
    get_encaissement_by_id,
    update_encaissement
)

st.title("Encaissements")

# =========================
# LISTE DES ENCAISSEMENTS
# =========================
st.subheader("Liste des encaissements")

encaissements = get_all_encaissements()

if encaissements:
    col1, col2, col3, col4, col5, col6 = st.columns([1,3,2,2,2,1])
    col1.markdown("**ID**")
    col2.markdown("**Donateur**")
    col3.markdown("**Date**")
    col4.markdown("**Montant**")
    col5.markdown("**Remarque**")
    col6.markdown("**Action**")

    for e in encaissements:
        col1, col2, col3, col4, col5, col6 = st.columns([1,3,2,2,2,1])

        col1.write(e[0])
        col2.write(e[1])
        col3.write(e[2])
        col4.write(e[3])
        col5.write(e[4])

        if col6.button("✏️", key=f"edit_enc_{e[0]}"):
            st.session_state["edit_encaissement_id"] = e[0]

else:
    st.info("Aucun encaissement enregistré.")

st.divider()

# =========================
# FORMULAIRE MODIFICATION
# =========================
if "edit_encaissement_id" in st.session_state:
    enc = get_encaissement_by_id(st.session_state["edit_encaissement_id"])

    st.subheader("✏️ Modifier l'encaissement")

    donateurs = get_donateurs_for_select()
    donateur_dict = {f"{d[0]} - {d[1]}": d[0] for d in donateurs}

    with st.form("form_edit_encaissement"):
        donateur_label = st.selectbox(
            "Donateur",
            list(donateur_dict.keys()),
            index=list(donateur_dict.values()).index(enc[1])
        )

        date_edit = st.date_input("Date", value=pd.to_datetime(enc[2]))
        montant_edit = st.number_input("Montant", min_value=0.0, value=float(enc[3]))
        remarque_edit = st.text_input("Remarque", value=enc[4] if enc[4] else "")

        submit_edit = st.form_submit_button("💾 Sauvegarder")

    if submit_edit:
        donateur_id = donateur_dict[donateur_label]

        update_encaissement(
            enc[0],
            donateur_id,
            str(date_edit),
            montant_edit,
            remarque_edit
        )

        st.success("Encaissement modifié avec succès !")
        del st.session_state["edit_encaissement_id"]
        st.rerun()

st.divider()

# =========================
# FORMULAIRE AJOUT
# =========================
st.subheader("Ajouter un encaissement")

donateurs = get_donateurs_for_select()
donateur_dict = {f"{d[0]} - {d[1]}": d[0] for d in donateurs}

with st.form("form_encaissement", clear_on_submit=True):
    donateur_label = st.selectbox("Donateur", list(donateur_dict.keys()))
    date_encaissement = st.date_input("Date", value=date.today())
    montant = st.number_input("Montant", min_value=0.0)
    remarque = st.text_input("Remarque (optionnel)")

    submit = st.form_submit_button("Enregistrer")


if submit:
        if montant < 0:
            st.warning("⚠️ Le montant ne peut pas être inférieur à zéro.")
        else:
            donateur_id = donateur_dict[donateur_label]
            add_encaissement(donateur_id, str(date_encaissement), montant, remarque)

            st.success("Encaissement ajouté avec succès !")
            st.rerun()
        '''
        # Réinitialiser les champs
        st.session_state.donateur_label = list(donateur_dict.keys())[0]
        st.session_state.date_encaissement = date.today()
        st.session_state.montant = 0.0
        st.session_state.remarque = ""
        '''
            