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

# Navigation function
def navigate(page):
    st.session_state["page"] = page

# App starts here
st.title("Willkommen bei NutriGPT")
st.subheader("Der Ernährungscoach für Ausdauersportler")

# Landing Page
if st.session_state["page"] == "landing":
    st.header("Bitte wähle eine Option")
    if st.button("Registrieren"):
        navigate("register")
    if st.button("Anmelden"):
        navigate("login")

# Registration Page
if st.session_state["page"] == "register":
    st.subheader("Registrierung")
    email = st.text_input("E-Mail-Adresse")
    password = st.text_input("Passwort", type="password")
    if st.button("Konto erstellen"):
        if email in user_data:
            st.error("Diese E-Mail ist bereits registriert.")
        else:
            hashed_pw = hash_password(password)
            verification_link = "https://example.com/verify?email=" + email
            send_verification_email(email, verification_link)
            user_data[email] = {"password": hashed_pw, "verified": False, "profile": {}}
            save_user_data()
            st.success("Registrierung abgeschlossen! Bitte überprüfe deine E-Mails, um dein Konto zu bestätigen.")
            navigate("data_collection")
    if st.button("Zurück zur Startseite"):
        navigate("landing")

# Data Collection Page
if st.session_state["page"] == "data_collection":
    st.subheader("Persönliche Daten erfassen")
    email = st.session_state.get("email", "")
    if email and email in user_data:
        profile = user_data[email].get("profile", {})
        name = st.text_input("Name:", value=profile.get("name", ""))
        gender = st.selectbox("Geschlecht:", ["Männlich", "Weiblich", "Andere"], index=0)
        age = st.number_input("Alter:", min_value=1, max_value=100, value=profile.get("age", 30), step=1)
        height = st.number_input("Größe (cm):", min_value=50.0, max_value=250.0, value=profile.get("height", 170.0), step=1.0)
        weight = st.number_input("Gewicht (kg):", min_value=20.0, max_value=200.0, value=profile.get("weight", 70.0), step=0.1)
        body_fat = st.number_input("Körperfettanteil (%):", min_value=0.0, max_value=100.0, value=profile.get("body_fat", 15.0), step=0.1)

        if st.button("Daten speichern"):
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
    if st.button("Zurück zur Startseite"):
        navigate("landing")

# Login Page
if st.session_state["page"] == "login":
    st.subheader("Anmeldung")
    email = st.text_input("E-Mail-Adresse (Anmeldung)")
    password = st.text_input("Passwort (Anmeldung)", type="password")
    if st.button("Einloggen"):
        if email not in user_data:
            st.error("Kein Konto mit dieser E-Mail gefunden.")
        elif not user_data[email].get("verified", False):
            st.error("Bitte bestätige zuerst deine E-Mail-Adresse.")
        elif user_data[email]["password"] != hash_password(password):
            st.error("Falsches Passwort.")
        else:
            st.success(f"Willkommen zurück, {email}!")
            st.session_state["email"] = email
            navigate("profile")
    if st.button("Zurück zur Startseite"):
        navigate("landing")

# Profile Page
if st.session_state["page"] == "profile":
    email = st.session_state.get("email", "")
    if email:
        st.subheader(f"Profil von {email}")
        profile = user_data[email].get("profile", {})
        st.write("Profil:", profile)
        if st.button("Profil bearbeiten"):
            navigate("data_collection")
        if st.button("Abmelden"):
            del st.session_state["email"]
            navigate("landing")
