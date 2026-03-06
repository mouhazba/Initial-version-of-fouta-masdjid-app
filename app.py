import streamlit as st
from pathlib import Path

DB_PATH = Path("database/database.db")

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Gestion du Ramadan", page_icon="🕌")

# =========================
# UTILISATEURS AUTORISÉS
# =========================
USERS = {
    "admin": "1234",
    "imam": "ramadan2026",
    "gestionnaire": "don2026"
}

# =========================
# INITIALISATION SESSION
# =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# =========================
# PAGE LOGIN
# =========================
st.title("🕌 Gestion des dons - Ramadan")
st.subheader("Connexion")

if not st.session_state.authenticated:

    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")

    if submit:
        if username in USERS and USERS[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Connexion réussie ✅")
            st.switch_page("pages/dashboard.py")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect ❌")

else:
    st.success(f"Bienvenue {st.session_state.username} 👋")
    if st.button("Aller au Dashboard"):
        st.switch_page("pages/dashboard.py")