import streamlit as st
from service.calculs import calcul_total_encaisse, calcul_total_depenses, calcul_solde, get_statut_tous_donateurs


# ======================
# authenticated
# ======================
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("⛔ Accès refusé. Veuillez vous connecter.")
    st.stop()

st.title("📊 Ramadan de Fouta Masdjid ")

# ======================
# deconnexion
# ======================
if st.button("🔓 Déconnexion"):
    st.session_state.authenticated = False
    st.switch_page("app.py")

# ======================
# Résumé financier
# ======================

total_encaisse = calcul_total_encaisse()
total_depenses = calcul_total_depenses()
solde = calcul_solde()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total encaissé", f"{total_encaisse} $")
col2.metric("💸 Total dépenses", f"{total_depenses} $")
col3.metric("🧾 Solde", f"{solde} $")

st.divider()

# ======================
# Statut des donateurs
# ======================

st.subheader("📋 Statut des donateurs")

donateurs_statut = get_statut_tous_donateurs()

nb_payes = len([d for d in donateurs_statut if d["statut"] == "Payé"])
nb_partiels = len([d for d in donateurs_statut if d["statut"] == "Partiel"])
nb_non_payes = len([d for d in donateurs_statut if d["statut"] == "Non payé"])

col4, col5, col6 = st.columns(3)
col4.metric("✅ Payés", nb_payes)
col5.metric("🟡 Partiels", nb_partiels)
col6.metric("❌ Non payés", nb_non_payes)

st.divider()

# ======================
# Tableau récapitulatif
# ======================

st.subheader("📑 Détail par donateur")

if donateurs_statut:
    st.dataframe(donateurs_statut)
else:
    st.info("Aucun donateur enregistré pour le moment.")