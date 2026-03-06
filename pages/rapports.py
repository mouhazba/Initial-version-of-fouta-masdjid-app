import streamlit as st
from service.calculs import rapport_journalier, rapport_mensuel, calcul_annuel
import matplotlib.pyplot as plt
import pandas as pd

# ======================
# authenticated
# ======================
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("⛔ Accès refusé. Veuillez vous connecter.")
    st.stop()


st.title("📊 Ramadan de Fouta Masdjid ")

st.header("📅 Rapport journalier")

date_rapport = st.date_input("Choisir une date")

if st.button("Générer rapport journalier"):
    date_str = date_rapport.strftime("%Y-%m-%d")

    rapport = rapport_journalier(date_str)

    st.success(f"Rapport du {date_str}")

    st.metric("💰 Total encaissé", rapport["total_encaisse"])
    st.metric("💸 Total dépenses", rapport["total_depenses"])
    st.metric("🧾 Solde du jour", rapport["solde"])

    st.subheader("Encaissements du jour")
    if rapport["encaissements"]:
        st.dataframe(rapport["encaissements"])
    else:
        st.info("Aucun encaissement pour cette date.")

    st.subheader("Dépenses du jour")
    if rapport["depenses"]:
        st.dataframe(rapport["depenses"])
    else:
        st.info("Aucune dépense pour cette date.")









# ======================
# RAPPORT MENSUEL
# ======================
st.subheader("🗓 Rapport mensuel")

annee = st.selectbox("Choisir l'année", [2024, 2025, 2026])
mois = st.selectbox("Choisir le mois", list(range(1, 13)))

if st.button("Générer rapport mensuel"):
    rapport = rapport_mensuel(annee, mois)

    st.success(f"Rapport du mois {mois}/{annee}")

    st.metric("💰 Total encaissé", rapport["total_encaisse"])
    st.metric("💸 Total dépenses", rapport["total_depenses"])
    st.metric("🧾 Solde du mois", rapport["solde"])

    st.subheader("Encaissements du mois")
    if rapport["encaissements"]:
        st.dataframe(rapport["encaissements"])
    else:
        st.info("Aucun encaissement pour ce mois.")

    st.subheader("Dépenses du mois")
    if rapport["depenses"]:
        st.dataframe(rapport["depenses"])
    else:
        st.info("Aucune dépense pour ce mois.")



    # ======================
# RAPPORT ANNUEL
# ======================
st.subheader("📆 Rapport annuel")

annee_annuelle = st.selectbox("Choisir l'année pour le rapport annuel", [2024, 2025, 2026], key="annee_annuelle")

if st.button("Générer rapport annuel"):
    encaissements, depenses, soldes = calcul_annuel(annee_annuelle)

    mois_labels = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
                   "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]

    st.success(f"Rapport annuel {annee_annuelle}")

    # ---- Graphique Encaissements
    st.subheader("📊 Encaissements par mois")
    fig1, ax1 = plt.subplots()
    ax1.bar(mois_labels, encaissements)
    st.pyplot(fig1)

    # ---- Graphique Dépenses
    st.subheader("📉 Dépenses par mois")
    fig2, ax2 = plt.subplots()
    ax2.bar(mois_labels, depenses)
    st.pyplot(fig2)

    # ---- Graphique Solde
    st.subheader("📈 Solde par mois")
    fig3, ax3 = plt.subplots()
    ax3.plot(mois_labels, soldes, marker="o")
    st.pyplot(fig3)