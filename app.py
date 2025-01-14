import streamlit as st
import json
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load or initialize the user database
USER_DB = "user_data.json"
try:
    with open(USER_DB, "r") as f:
        user_data = json.load(f)
except FileNotFoundError:
    user_data = {}

# Save user data to file
def save_user_data():
    with open(USER_DB, "w") as f:
        json.dump(user_data, f)

# Email verification
def send_verification_email(email, verification_link):
    sender_email = "jorge@jorge-sports.com"
    sender_password = "Capoeira72!Jorge!"
    smtp_server = "smtp.strato.de"
    smtp_port = 587

    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Bitte bestätige deine Registrierung bei NutriGPT"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Bitte klicke auf den folgenden Link, um deine Registrierung abzuschließen: {verification_link}"
    html = f"<html><body><p>Bitte klicke auf den folgenden Link, um deine Registrierung abzuschließen: <a href='{verification_link}'>Bestätigen</a></p></body></html>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        st.error(f"Fehler beim Senden der E-Mail: {e}")

# Hashing passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "landing"
if "role" not in st.session_state:
    st.session_state["role"] = None

# Navigation function
def navigate(page):
    st.session_state["page"] = page

# App starts here
st.title("Willkommen bei NutriGPT")
st.subheader("Der Ernährungscoach für Ausdauersportler")

# Landing Page
if st.session_state["page"] == "landing":
    st.header("Bitte wähle eine Option")
    if st.button("Registrieren", key="register_button"):
        navigate("register")
    if st.button("Anmelden", key="login_button"):
        navigate("login")
    if st.button("Admin", key="admin_button"):
        navigate("admin")

# Registration Page
if st.session_state["page"] == "register":
    st.subheader("Registrierung")
    email = st.text_input("E-Mail-Adresse", key="register_email")
    password = st.text_input("Passwort", type="password", key="register_password")
    if st.button("Konto erstellen", key="create_account"):
        if email in user_data:
            st.error("Diese E-Mail ist bereits registriert.")
        else:
            hashed_pw = hash_password(password)
            verification_link = f"https://nutrigpt.streamlit.app/?page=verify&email={email}"
            send_verification_email(email, verification_link)
            user_data[email] = {
                "password": hashed_pw, "verified": False, "profile": {}, "role": "user"
            }
            save_user_data()
            st.success("Registrierung abgeschlossen! Bitte überprüfe deine E-Mails, um dein Konto zu bestätigen.")
    if st.button("Zurück zur Startseite", key="back_to_landing"):
        navigate("landing")

# Verification Page
if st.session_state["page"] == "verify":
    query_params = st.experimental_get_query_params()
    email = query_params.get("email", [None])[0]
    if email and email in user_data:
        user_data[email]["verified"] = True
        save_user_data()
        st.success(f"Danke, {email}! Dein Konto wurde erfolgreich verifiziert.")
        navigate("login")
    else:
        st.error("Ungültiger Verifizierungslink.")
        navigate("landing")

# Data Collection Page
if st.session_state["page"] == "data_collection":
    st.subheader("Persönliche Daten erfassen")
    email = st.session_state.get("email", "")
    if email and email in user_data:
        profile = user_data[email].get("profile", {})
        name = st.text_input("Name:", value=profile.get("name", ""), key="data_name")
        gender = st.selectbox("Geschlecht:", ["Männlich", "Weiblich", "Andere"], index=0, key="data_gender")
        age = st.number_input("Alter:", min_value=1, max_value=100, value=profile.get("age", 30), step=1, key="data_age")
        height = st.number_input("Größe (cm):", min_value=50.0, max_value=250.0, value=profile.get("height", 170.0), step=1.0, key="data_height")
        weight = st.number_input("Gewicht (kg):", min_value=20.0, max_value=200.0, value=profile.get("weight", 70.0), step=0.1, key="data_weight")
        body_fat = st.number_input("Körperfettanteil (%):", min_value=0.0, max_value=100.0, value=profile.get("body_fat", 15.0), step=0.1, key="data_body_fat")

        if st.button("Daten speichern", key="save_data"):
            user_data[email]["profile"] = {
                "name": name,
                "gender": gender,
                "age": age,
                "height": height,
                "weight": weight,
                "body_fat": body_fat,
            }
            save_user_data()
            st.success("Daten wurden gespeichert! Weiterleitung zum Profil...")
            navigate("profile")
    if st.button("Zurück zur Startseite", key="back_to_landing_from_data"):
        navigate("landing")

# Login Page
if st.session_state["page"] == "login":
    st.subheader("Anmeldung")
    email = st.text_input("E-Mail-Adresse (Anmeldung)", key="login_email")
    password = st.text_input("Passwort (Anmeldung)", type="password", key="login_password")
    if st.button("Einloggen", key="login_button_submit"):
        if email not in user_data:
            st.error("Kein Konto mit dieser E-Mail gefunden.")
        elif not user_data[email].get("verified", False):
            st.error("Bitte bestätige zuerst deine E-Mail-Adresse.")
        elif user_data[email]["password"] != hash_password(password):
            st.error("Falsches Passwort.")
        else:
            st.success(f"Willkommen zurück, {email}!")
            st.session_state["email"] = email
            st.session_state["role"] = user_data[email].get("role", "user")
            navigate("profile")
    if st.button("Zurück zur Startseite", key="back_to_landing_from_login"):
        navigate("landing")

# Profile Page
if st.session_state["page"] == "profile":
    email = st.session_state.get("email", "")
    role = st.session_state.get("role", "user")
    if email:
        st.subheader(f"Profil von {email}")
        profile = user_data[email].get("profile", {})
        st.write("Profil:", profile)
        if role == "admin":
            st.write("Du hast Admin-Rechte.")
        if st.button("Profil bearbeiten", key="edit_profile"):
            navigate("data_collection")
        if st.button("Abmelden", key="logout"):
            del st.session_state["email"]
            del st.session_state["role"]
            navigate("landing")

# Admin Page
if st.session_state["page"] == "admin":
    email = st.session_state.get("email", "")
    role = st.session_state.get("role", "user")
    if role == "admin":
        st.subheader("Admin-Bereich")
        st.write("Benutzerliste:")
        for user, details in user_data.items():
            st.write(f"E-Mail: {user}")
            st.write(f"Verifiziert: {details.get('verified', False)}")
            st.write("Profil:", details.get("profile", {}))
            if st.button(f"Benutzer löschen: {user}", key=f"delete_{user}"):
                del user_data[user]
                save_user_data()
                st.success(f"Benutzer {user} wurde gelöscht.")
    else:
        st.error("Du hast keine Berechtigung, diese Seite anzuzeigen.")
        navigate("landing")
