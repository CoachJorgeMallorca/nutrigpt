import streamlit as st
import hashlib

# NutriGPT: Virtual Nutrition Coach
st.title("NutriGPT - Dein Ernährungscoach für Ausdauersportler")
st.subheader("Individuelle Ernährungspläne für deine Trainingsziele")

# Prompt Explanation
st.write("Hallo! Ich bin NutriGPT, dein virtueller Ernährungscoach. Ich helfe dir, deine Ernährung optimal an deine Trainingsziele anzupassen. Lass uns starten!")

# Collect biometric data
gender = st.selectbox("Geschlecht:", ["Männlich", "Weiblich", "Andere"], index=0)
age = st.number_input("Alter:", min_value=1, max_value=100, value=30, step=1)
height = st.number_input("Größe (cm):", min_value=50.0, max_value=250.0, value=170.0, step=1.0)
weight = st.number_input("Gewicht (kg):", min_value=20.0, max_value=200.0, value=70.0, step=0.1)
body_fat = st.number_input("Körperfettanteil (%):", min_value=0.0, max_value=100.0, value=15.0, step=0.1)

# Collect performance data
ftp = st.number_input("FTP (Watt):", min_value=0.0, max_value=500.0, value=200.0, step=0.1)
vo2max = st.number_input("VO2max (ml/kg/min):", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
vlamax = st.number_input("VLamax (mmol/l/s):", min_value=0.0, max_value=1.0, value=0.6, step=0.01)
fatmax = st.number_input("Fatmax (Watt):", min_value=0.0, max_value=500.0, value=150.0, step=0.1)

# Goals and timeline
goal = st.multiselect(
    "Ziele:",
    [
        "Volkstriathlon", "Olympische Distanz Triathlon", "Mitteldistanz Triathlon", "Langdistanz Triathlon",
        "Marathon", "Radmarathon", "Abnehmen", "Gewicht halten", "Muskelaufbau", "Leistung steigern",
        "Fettstoffwechsel verbessern", "VO2max steigern", "VLamax senken"
    ],
    default=["Abnehmen"]
)
timeline = st.text_input("Wann möchtest du dein Ziel erreichen? (z. B. 'In 3 Monaten', 'Bis zum nächsten Wettkampf')")

# PAL-Wert
deficit = st.slider("Kaloriendefizit (maximal 500 kcal empfohlen):", min_value=0, max_value=500, value=300, step=50)
pal = st.number_input("PAL-Wert (Physical Activity Level):", min_value=1.0, max_value=2.5, value=1.2, step=0.1)

# Training plans
st.write("### Trainingsplanung")
workout_today = st.text_input("Trainingseinheit heute (z. B. 60min Laufen GA1):")
workout_tomorrow = st.text_input("Trainingseinheit morgen (z. B. 90min Radfahren mit 3x10min EB):")

def calculate_tdee(weight, height, age, gender, pal):
    tdee = (10 * weight) + (6.25 * height) - (5 * age)
    tdee += 5 if gender == "Männlich" else -161
    return tdee * pal

def calculate_training_calories(activity, duration, intensity, weight):
    if activity == "Laufen":
        pace_factor = {
            "GA1": 0.8, "GA2": 0.9, "SWB": 1.0, "EB": 1.1, "WSA": 1.2
        }.get(intensity, 1.0)
        return duration * (weight * pace_factor)
    elif activity == "Radfahren":
        ftp_factor = {
            "REKOM": 0.5, "GA1": 0.75, "GA2": 0.9, "SWB": 1.0, "EB": 1.2, "WSA": 1.4
        }.get(intensity, 1.0)
        return duration * (ftp * ftp_factor)
    elif activity == "Schwimmen":
        pace_factor = {
            "schnell": 0.15, "mittel": 0.18, "langsam": 0.20
        }.get(intensity, 0.18)
        return duration * (weight * pace_factor)
    return 0

# Calculate total daily energy expenditure
tdee = calculate_tdee(weight, height, age, gender, pal)
training_calories_today = calculate_training_calories("Laufen", 60, "GA1", weight)
training_calories_tomorrow = calculate_training_calories("Radfahren", 90, "GA2", weight)
total_calories_today = tdee + training_calories_today - deficit

def generate_meal_plan():
    return {
        "Frühstück": "Haferflocken (30g), Milch (200ml), Banane (1)",
        "Mittagessen": "Hähnchenbrust (150g), Gemüse (200g), Reis (50g)",
        "Abendessen": "Eier (2), Vollkornbrot (50g), Avocado (1/2)",
        "Snacks": "Recovery-Shake (30g Protein, 60g Kohlenhydrate)"
    }

if st.button("Ernährungsplan erstellen"):
    meal_plan = generate_meal_plan()
    st.write("### Dein Tagesbedarf")
    st.write(f"Grundumsatz: {tdee:.2f} kcal")
    st.write(f"Trainingseinheiten heute: {training_calories_today:.2f} kcal")
    st.write(f"Kalorienziel (inkl. Defizit): {total_calories_today:.2f} kcal")

    st.write("### Dein Ernährungsplan")
    for meal, desc in meal_plan.items():
        st.write(f"- **{meal}:** {desc}")

    st.write("### Empfehlungen für Snacks")
    st.write("- Recovery-Shake: 60g Kohlenhydrate, 30g Protein (ca. 350 kcal)")
