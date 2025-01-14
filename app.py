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
st.title("NutriGPT - Mitgliederverwaltung")

# Step 1: User identification
st.header("1. Willkommen zurück oder Neues Profil erstellen")
username = st.text_input("Wie heißt du?", key="username")

if username:
    if username in user_data:
        st.success(f"Willkommen zurück, {username}!")
        # Check for updates in weight or body fat
        if st.checkbox("Haben sich Gewicht oder Körperfettanteil geändert?"):
            user_data[username]["weight"] = st.number_input("Aktuelles Gewicht (kg):", value=user_data[username]["weight"], step=0.1)
            user_data[username]["body_fat"] = st.number_input("Aktueller Körperfettanteil (%):", value=user_data[username]["body_fat"], step=0.1)
            save_user_data()
            st.success("Daten aktualisiert!")
    else:
        st.info(f"Neues Profil für {username} erstellen.")
        gender = st.selectbox("Geschlecht:", ["Männlich", "Weiblich", "Andere"])
        age = st.number_input("Alter:", min_value=1, max_value=100, value=30, step=1)
        height = st.number_input("Größe (cm):", min_value=50, max_value=250, value=170, step=1)
        weight = st.number_input("Gewicht (kg):", min_value=20.0, max_value=200.0, value=70.0, step=0.1)
        body_fat = st.number_input("Körperfettanteil (%):", min_value=0.0, max_value=100.0, value=15.0, step=0.1)

        if st.button("Profil erstellen"):
            user_data[username] = {
                "gender": gender,
                "age": age,
                "height": height,
                "weight": weight,
                "body_fat": body_fat,
            }
            save_user_data()
            st.success(f"Profil für {username} wurde erstellt!")

# Display stored data for debugging or review
if st.checkbox("Gespeicherte Benutzer anzeigen"):
    st.json(user_data)
