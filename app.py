import streamlit as st

# -----------------------------
# Hilfsfunktionen
# -----------------------------

def berechne_grundumsatz_harris_benedict(geschlecht, gewicht, groesse, alter):
    """
    Harris-Benedict-Formel:
    Männer:  66,47 + (13,7 x Gewicht in kg) + (5 x Größe in cm) - (6,8 x Alter)
    Frauen: 655,1 + (9,6 x Gewicht in kg)   + (1,8 x Größe in cm) - (4,7 x Alter)
    """
    if geschlecht.lower() in ["m", "mann", "male"]:
        grundumsatz = 66.47 + (13.7 * gewicht) + (5 * groesse) - (6.8 * alter)
    else:
        grundumsatz = 655.1 + (9.6 * gewicht) + (1.8 * groesse) - (4.7 * alter)
    return round(grundumsatz, 2)

def berechne_arbeitsumsatz(grundumsatz, pal):
    """Berechnet den Gesamtumsatz: Grundumsatz * PAL."""
    return round(grundumsatz * pal, 2)

def antworte_auf_nachricht(user_msg, user_data):
    """
    Kernlogik, die auf Basis des Prompts und der Nutzerdaten antwortet.
    user_data ist ein Dictionary mit allen relevanten Infos.
    """
    # Fiktive Beispielantwort, die die Daten auswertet.
    # Im echten Einsatz würdest du hier weitere Berechnungen
    # und Empfehlungen (z. B. aus dem Prompt) integrieren.
    
    if "grundumsatz" not in user_data:
        return (
            "Ich habe noch nicht alle Daten von dir. "
            "Bitte trage erst alle notwendigen Angaben ein."
        )
    
    # Beispiel: Überprüfen, ob der User nach 'Kalorienbedarf' gefragt hat
    if "kalorienbedarf" in user_msg.lower():
        return (
            f"Dein geschätzter Grundumsatz liegt bei {user_data['grundumsatz']} kcal. "
            f"Dein Gesamtumsatz (inkl. PAL von {user_data['pal']}) liegt bei "
            f"{user_data['arbeitsumsatz']} kcal.\n\n"
            "Falls du dein Gewicht halten möchtest, ist das dein grober Tagesbedarf. "
            "Für Muskelaufbau und höhere Leistungsziele können wir "
            "die Kalorienaufnahme entsprechend anpassen."
        )
    
    # Beispiel-Antwort auf eine andere Frage
    if "Hallo" in user_msg or "Servus" in user_msg or "Moin" in user_msg:
        return (
            "Hallo! Wie kann ich dir heute weiterhelfen? Vielleicht willst du mehr "
            "über deinen Kohlenhydratbedarf vor dem Training wissen?"
        )
    
    # Fallback-Antwort
    return (
        "Danke für deine Nachricht! Ich bin hier, um deine Fragen rund um "
        "Ernährung und Training zu beantworten. Versuche es mit einer konkreten Frage, "
        "z. B. 'Wie hoch ist mein Kalorienbedarf?' oder 'Wie sieht eine "
        "typische Recovery-Mahlzeit aus?'"
    )

# -----------------------------
# Streamlit-App
# -----------------------------

def main():
    st.set_page_config(page_title="NutriGPT", layout="centered")
    st.title("NutriGPT: Virtueller Ernährungscoach")
    st.write(
        "Willkommen bei NutriGPT! Ich helfe dir, deine Ernährung auf "
        "deine Trainingsziele abzustimmen. "
        "Gib deine Daten ein und starte das Chat-Gespräch."
    )

    # Session State für Nachrichten und Benutzerdaten
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "user_data" not in st.session_state:
        st.session_state["user_data"] = {}

    # -----------------------------
    # Dateneingabe
    # -----------------------------
    with st.form("dateneingabe"):
        geschlecht = st.selectbox("Geschlecht", ["Männlich", "Weiblich"])
        alter = st.number_input("Alter (Jahre)", min_value=1, max_value=120, value=30)
        groesse = st.number_input("Größe (cm)", min_value=100, max_value=250, value=180)
        gewicht = st.number_input("Gewicht (kg)", min_value=30.0, max_value=250.0, value=75.0)
        koerperfett = st.number_input("Körperfettanteil (%)", min_value=0.0, max_value=60.0, value=15.0)
        pal = st.selectbox(
            "PAL-Wert (Physical Activity Level)",
            [("Sitzend / kaum Bewegung", 1.2),
             ("Sitzend / wenig Bewegung", 1.4),
             ("Stehend / gehend", 1.6),
             ("Körperlich anstrengende Arbeit", 1.8)]
        )

        # Leistungsdaten
        ftp = st.number_input("FTP (Watt)", min_value=0, max_value=600, value=200)
        vo2max = st.number_input("VO2max (ml/min/kg)", min_value=0.0, max_value=90.0, value=50.0)
        vlamax = st.number_input("VLamax (mmol/l/s)", min_value=0.0, max_value=2.0, value=0.5)
        fatmax = st.number_input("Fatmax (kcal/h)", min_value=0.0, max_value=1500.0, value=300.0)

        ziel = st.multiselect(
            "Ziele",
            ["Volkstriathlon", "Olympische Distanz", "Mitteldistanz", "Langdistanz",
             "Marathon", "Radmarathon", "Abnehmen", "Gewicht halten", "Muskelaufbau",
             "Fettstoffwechsel verbessern", "VO2max steigern", "VLamax senken"]
        )

        zeitlicher_rahmen = st.text_input("Zeitlicher Rahmen (z.B. Wettkampfdatum, Abnehmziel etc.)")

        training_heute = st.text_area("Geplante Einheit(en) HEUTE (z.B. 60min Laufen GA1)")
        training_morgen = st.text_area("Geplante Einheit(en) MORGEN (z.B. 90min Rad GA2)")

        # Beim Klick auf den Absenden-Button werden Daten übernommen
        submitted = st.form_submit_button("Daten übernehmen")
        if submitted:
            # Harris-Benedict
            grundumsatz = berechne_grundumsatz_harris_benedict(
                geschlecht, gewicht, groesse, alter
            )
            arbeitsumsatz = berechne_arbeitsumsatz(grundumsatz, pal[1])

            st.session_state["user_data"] = {
                "geschlecht": geschlecht,
                "alter": alter,
                "groesse": groesse,
                "gewicht": gewicht,
                "kfa": koerperfett,
                "pal": pal[1],
                "ftp": ftp,
                "vo2max": vo2max,
                "vlamax": vlamax,
                "fatmax": fatmax,
                "ziel": ziel,
                "zeitlicher_rahmen": zeitlicher_rahmen,
                "training_heute": training_heute,
                "training_morgen": training_morgen,
                "grundumsatz": grundumsatz,
                "arbeitsumsatz": arbeitsumsatz
            }

            st.success("Daten übernommen! Du kannst nun im Chat weiter unten fragen stellen.")

    # -----------------------------
    # Chat-Bereich
    # -----------------------------
    st.write("---")
    st.header("NutriGPT-Chat")
    user_input = st.text_input("Deine Nachricht:")
    if st.button("Senden"):
        # Speichere User-Nachricht
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Generiere Antwort
        nutri_antwort = antworte_auf_nachricht(user_input, st.session_state["user_data"])
        st.session_state["messages"].append({"role": "assistant", "content": nutri_antwort})

    # Chat-Verlauf anzeigen
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            st.markdown(f"**NutriGPT**: {msg['content']}")
        else:
            st.markdown(f"**Du**: {msg['content']}")

if __name__ == "__main__":
    main()
