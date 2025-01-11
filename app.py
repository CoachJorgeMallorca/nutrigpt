import streamlit as st

# Begrüßung
st.title("NutriGPT - Dein virtueller Ernährungscoach")
st.subheader("Erstelle deinen individuellen Ernährungsplan für optimale Performance")

# Schritt 1: Persönliche Daten
st.header("1. Persönliche Daten")
name = st.text_input("Wie heißt du?")
age = st.number_input("Wie alt bist du?", min_value=1, max_value=100, value=30)
weight = st.number_input("Wie viel wiegst du (in kg)?", min_value=20.0, max_value=200.0, value=70.0, step=0.1)
height = st.number_input("Wie groß bist du (in cm)?", min_value=50.0, max_value=250.0, value=170.0, step=0.1)
body_fat = st.number_input("Körperfettanteil (in %)?", min_value=0.0, max_value=100.0, value=15.0, step=0.1)

# Schritt 2: Leistungsdaten
st.header("2. Leistungsdaten")
ftp = st.number_input("FTP (Radfahren) in Watt:", min_value=0, max_value=1000, value=200)
vo2max = st.number_input("VO2max in ml/O2/kg:", min_value=0.0, max_value=100.0, value=45.0, step=0.1)
vlamax = st.number_input("VLamax in mmol/l/s:", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
fatmax = st.number_input("Fatmax in Watt (falls bekannt):", min_value=0, max_value=500, value=120)

# Schritt 3: Trainingsplanung
st.header("3. Trainingsplanung")
today_workout = st.text_area("Heutiges Workout (z. B. 90 Min Rad GA1):")
tomorrow_workout = st.text_area("Morgiges Workout (z. B. 60 Min Laufen mit 5x4 Min EB):")

# Schritt 4: Ziele definieren
st.header("4. Ziele definieren")
goal = st.selectbox(
    "Was möchtest du erreichen?",
    ["Abnehmen", "Gewicht halten", "Muskeln aufbauen", "Leistung steigern", "Fettstoffwechsel verbessern", "Kombination"]
)
time_frame = st.number_input("In welchem Zeitraum möchtest du dein Ziel erreichen (in Tagen)?", min_value=1, value=30)

# Daten auswerten
if st.button("Plane meine Ernährung"):
    # Beispielauswertung
    st.success(f"Hallo {name}, basierend auf deinen Daten werde ich deinen Ernährungsplan erstellen!")
    st.write(f"Alter: {age} Jahre | Gewicht: {weight} kg | Größe: {height} cm | Körperfett: {body_fat}%")
    st.write(f"Ziel: {goal} in {time_frame} Tagen")
    st.write("Deine heutigen Trainingseinheiten:", today_workout)
    st.write("Deine morgigen Trainingseinheiten:", tomorrow_workout)

    # Placeholder für weitere Logik (z. B. Berechnungen und Rezeptausgabe)
    st.info("Weitere Funktionen wie Mahlzeitenplanung und PDF-Erstellung kommen hier später hinzu!")

# Abschluss
st.write("💡 Teste NutriGPT weiter und lass uns gemeinsam optimieren!")
