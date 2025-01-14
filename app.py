import streamlit as st
import hashlib

# NutriGPT Prompt-based Script without user management

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

st.title("NutriGPT - Dein Ernährungscoach für Ausdauersportler")
st.subheader("Individuelle Ernährungspläne, perfekt abgestimmt auf deine Ziele und Workouts")

# Prompt Explanation
st.write("Hallo! Ich bin NutriGPT, dein virtueller Ernährungscoach. Ich helfe dir, deine Ernährung optimal an deine Trainingsziele anzupassen. Lass uns starten!")

# Collect biometric data
gender = st.selectbox("Geschlecht:", ["Männlich", "Weiblich", "Andere"], index=0)
age = st.number_input("Alter:", min_value=1, max_value=100, value=30, step=1)
height = st.number_input("Größe (cm):", min_value=50.0, max_value=250.0, value=170.0, step=1.0)
weight = st.number_input("Gewicht (kg):", min_value=20.0, max_value=200.0, value=70.0, step=0.1)
body_fat = st.number_input("Körperfettanteil (%):", min_value=0.0, max_value=100.0, value=15.0, step=0.1)

# Training information
st.write("Jetzt benötige ich Informationen zu deinem Training:")
workout_today = st.text_input("Trainingseinheit heute (z. B. 60min Laufen GA1):")
workout_tomorrow = st.text_input("Trainingseinheit morgen (z. B. 90min Radfahren mit 3x10min EB):")

goal = st.selectbox("Ziel:", ["Abnehmen", "Gewicht halten", "Muskelaufbau", "Fettstoffwechsel verbessern", "Leistung steigern"])
deficit = st.slider("Kaloriendefizit (maximal 500 kcal empfohlen):", min_value=0, max_value=500, value=300, step=50)

# Calculate daily energy expenditure
tdee = (10 * weight) + (6.25 * height) - (5 * age)
if gender == "Männlich":
    tdee += 5
else:
    tdee -= 161

def calc_meals(deficit, tdee):
    net_calories = tdee - deficit
    meals = {
        "Frühstück": "30g Haferflocken, 200ml Milch, 1 Banane (ca. 300 kcal)",
        "Mittagessen": "150g Hähnchenbrust, 200g Gemüse, 50g Reis (ca. 400 kcal)",
        "Abendessen": "2 Eier, 50g Vollkornbrot, 1 Avocado (ca. 350 kcal)",
        "Vor dem Training": "Schwarzer Kaffee mit MCT-Öl (ca. 50 kcal)",
        "Nach dem Training": "Recovery-Shake (30g Protein, 60g Kohlenhydrate, ca. 350 kcal)"
    }
    return net_calories, meals

# Output nutrition plan
if st.button("Ernährungsplan erstellen"):
    net_calories, meals = calc_meals(deficit, tdee)

    st.write("### Dein Tagesbedarf")
    st.write(f"Grundumsatz: {tdee:.2f} kcal")
    st.write(f"Mit deinem Kaloriendefizit: {net_calories:.2f} kcal")

    st.write("### Empfehlungen für Mahlzeiten")
    for meal, desc in meals.items():
        st.write(f"- **{meal}:** {desc}")
