import streamlit as st
import json

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

# App starts here
st.title("Willkommen bei NutriGPT")
st.subheader("Der Ernährungscoach für Ausdauersportler")

# Landing Page
st.header("Bitte melde dich an oder erstelle ein neues Profil")

# Step 1: Login or Registration
email = st.text_input("E-Mail-Adresse", key="email")
if email:
    if email in user_data:
        st.success(f"Willkommen zurück, {email}!")
    else:
        st.info("Neue Registrierung erforderlich.")
        if st.button("Profil erstellen"):
            user_data[email] = {}
            save_user_data()
            st.success(f"Profil für {email} wurde erstellt! Bitte fahre mit der Datenerfassung fort.")

# Proceed to Data Collection
if email in user_data and st.button("Weiter zur Datenerfassung"):
    st.write("\n## Persönliche Daten erfassen")
    name = st.text_input("Name:", value=user_data[email].get("name", ""))
    gender = st.selectbox("Geschlecht:", ["Männlich", "Weiblich", "Andere"], index=0)
    age = st.number_input("Alter:", min_value=1, max_value=100, value=user_data[email].get("age", 30), step=1)
    height = st.number_input("Größe (cm):", min_value=50.0, max_value=250.0, value=user_data[email].get("height", 170.0), step=1.0)
    weight = st.number_input("Gewicht (kg):", min_value=20.0, max_value=200.0, value=user_data[email].get("weight", 70.0), step=0.1)
    body_fat = st.number_input("Körperfettanteil (%):", min_value=0.0, max_value=100.0, value=user_data[email].get("body_fat", 15.0), step=0.1)

    if st.button("Daten speichern"):
        user_data[email] = {
            "name": name,
            "gender": gender,
            "age": age,
            "height": height,
            "weight": weight,
            "body_fat": body_fat,
        }
        save_user_data()
        st.success("Daten wurden gespeichert!")

