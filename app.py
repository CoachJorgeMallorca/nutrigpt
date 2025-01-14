import streamlit as st
import math

# -----------------------------
# 1. Begrüßung
# -----------------------------
def begruessung():
    st.title("NutriGPT - Dein virtueller Ernährungscoach für Ausdauersport")
    st.write(
        "Hallo! Ich bin NutriGPT, dein virtueller Ernährungscoach. "
        "Ich helfe dir, deine Ernährung optimal an deine Trainingsziele anzupassen. "
        "Lass uns gemeinsam starten!"
    )

# -----------------------------
# 2. Datenerfassung
# -----------------------------

def berechne_grundumsatz_harris_benedict(geschlecht, gewicht, groesse, alter):
    """
    Harris-Benedict-Formel:
    Männer:  66,47 + (13,7 x Gewicht in kg) + (5 x Größe in cm) - (6,8 x Alter)
    Frauen: 655,1 + (9,6 x Gewicht in kg)   + (1,8 x Größe in cm) - (4,7 x Alter)
    """
    if geschlecht.lower() in ["männlich", "mann", "male", "m"]:
        grundumsatz = 66.47 + (13.7 * gewicht) + (5.0 * groesse) - (6.8 * alter)
    else:
        grundumsatz = 655.1 + (9.6 * gewicht) + (1.8 * groesse) - (4.7 * alter)
    return round(grundumsatz, 2)

def parse_lauftraining(angabe, gewicht):
    """
    Sehr vereinfachte Berechnung:
    - Wir suchen nach 'XXmin Laufen GAx'
    - Pace: 6:00 min/km, also 10 km/h bei 60min => 10km => 1kcal/kg/km
    - Multiplikatoren je nach Intensität (GA1, GA2, EB, WSA etc.) nur rudimentär hier.
    """
    # Standardwerte:
    km_pro_min = 1.0 / 6.0  # 6 min pro km -> ~0.1667 km/min

    zeit_min = 0
    intensitaet = "GA1"

    # Zeit herausfiltern
    try:
        # Split am "min"
        splitted = angabe.lower().split("min")
        zeit_min = int(splitted[0].strip())
    except:
        zeit_min = 0

    # Intensität filtern (sehr einfach)
    if "ga2" in angabe.lower():
        intensitaet = "GA2"
    elif "eb" in angabe.lower():
        intensitaet = "EB"
    elif "wsa" in angabe.lower():
        intensitaet = "WSA"
    elif "swb" in angabe.lower():
        intensitaet = "SWB"

    # km errechnen
    km = zeit_min * km_pro_min

    # Basis: 1 kcal pro kg pro km
    # Zusätzliche Multiplikatoren: (Beispielwerte!)
    multiplikator = 1.0
    if intensitaet == "GA2":
        multiplikator = 1.2
    elif intensitaet == "swb":
        multiplikator = 1.3
    elif intensitaet == "eb":
        multiplikator = 1.4
    elif intensitaet == "wsa":
        multiplikator = 1.5

    kcal = km * gewicht * multiplikator
    return round(kcal, 2)

def parse_radtraining(angabe, ftp):
    """
    Vereinfachte Beispielrechnung. 
    OFFIZIELL: 1W = 1 J/s = 3,6 kJ/h ~ 0,86 kcal/h => 1 Watt ~3,865 kcal/h
    Trainingsbereiche (Angabe in Prompt):
      REKOM = FTP - 50%
      GA1 = FTP - 25-40%
      GA2 = FTP - 10-25%
      SWB = FTP -0-10%
      EB = FTP +5-20%
      WSA / SB = FTP +25-40%

    Wir parsen z.B. "90min Rad GA2".
    Nehmen wir an, wir fahren mit x% der FTP.
    Hier stark vereinfacht: 
      GA1 => ~ 70% FTP 
      GA2 => ~ 85% FTP 
      EB => ~ 105% FTP 
      WSA => ~ 125% FTP 
    """
    zeit_min = 0
    intensitaet = "GA1"
    try:
        splitted = angabe.lower().split("min")
        zeit_min = int(splitted[0].strip())
    except:
        zeit_min = 0

    if "ga2" in angabe.lower():
        intensitaet = "GA2"
    elif "eb" in angabe.lower():
        intensitaet = "EB"
    elif "wsa" in angabe.lower():
        intensitaet = "WSA"
    elif "swb" in angabe.lower():
        intensitaet = "SWB"
    elif "rekom" in angabe.lower():
        intensitaet = "REKOM"

    # einfache Annahmen
    if intensitaet == "REKOM":
        watt = ftp * 0.5
    elif intensitaet == "ga1":
        watt = ftp * 0.7
    elif intensitaet == "ga2":
        watt = ftp * 0.85
    elif intensitaet == "swb":
        watt = ftp * 0.95
    elif intensitaet == "eb":
        watt = ftp * 1.05
    elif intensitaet == "wsa":
        watt = ftp * 1.25
    else:
        watt = ftp * 0.7  # fallback

    stunden = zeit_min / 60.0
    kcal = watt * 3.865 * stunden  # grobe Umrechnung
    return round(kcal, 2)

def parse_schwimmtraining(angabe, zeit400m):
    """
    Beispiel-Schätzung basierend auf 400m-Zeit. 
    - Grobe Annahme: 60 min moderates Schwimmen ~ 500 kcal, 
      variiert je nach Intensität.
    - Wer 400m in 8min schwimmt, hat anders Tempo als 400m in 6min.
    """
    zeit_min = 0
    try:
        splitted = angabe.lower().split("min")
        zeit_min = int(splitted[0].strip())
    except:
        zeit_min = 0

    # relative Intensität => z. B. 400m in 6min => flotter als 400m in 8min
    # Hier Bastelwert: 
    basis_kcal_pro_min = 8.0  # moderate Intensität
    if zeit400m < 6:
        basis_kcal_pro_min = 10.0
    elif zeit400m > 8:
        basis_kcal_pro_min = 6.0

    # Suche nach intensität (z.B. EB, WSA etc.)
    intensitaet = "GA"
    if "eb" in angabe.lower():
        intensitaet = "EB"
    elif "wsa" in angabe.lower():
        intensitaet = "WSA"
    elif "ga2" in angabe.lower():
        intensitaet = "GA2"

    # Zusätzlicher Multiplikator
    multi = 1.0
    if intensitaet == "eb":
        multi = 1.2
    elif intensitaet == "wsa":
        multi = 1.3
    elif intensitaet == "ga2":
        multi = 1.1

    kcal = zeit_min * basis_kcal_pro_min * multi
    return round(kcal, 2)

def energie_verbrauch(heute, morgen, gewicht, ftp, zeit400m):
    """
    Liest die Eingabe-Strings für heute und morgen aus, 
    berechnet Kcal, gibt nur die Kcal von HEUTE zurück
    (weil laut Prompt geht's um Tagesbedarf).
    """
    kcal_heute = 0.0
    kcal_morgen = 0.0

    # Heutige Einheit(en) -> Zeilenweise trennen
    if heute:
        trainings = heute.split("\n")
        for t in trainings:
            t_lower = t.lower()
            if "laufen" in t_lower:
                kcal_heute += parse_lauftraining(t, gewicht)
            elif "rad" in t_lower or "bike" in t_lower:
                kcal_heute += parse_radtraining(t, ftp)
            elif "schwimm" in t_lower:
                kcal_heute += parse_schwimmtraining(t, zeit400m)

    # Die morgige Einheit wird nur vermerkt, könnte man für 
    # Carbo-Load-Empfehlung oder dergleichen nutzen
    if morgen:
        trainings = morgen.split("\n")
        for t in trainings:
            t_lower = t.lower()
            if "laufen" in t_lower:
                kcal_morgen += parse_lauftraining(t, gewicht)
            elif "rad" in t_lower or "bike" in t_lower:
                kcal_morgen += parse_radtraining(t, ftp)
            elif "schwimm" in t_lower:
                kcal_morgen += parse_schwimmtraining(t, zeit400m)

    return round(kcal_heute, 2), round(kcal_morgen, 2)

# -----------------------------
# 3. Trainingsplanung & 4. Ernährungsstrategie
# -----------------------------
def erstelle_ernaehrungsplan(user_data):
    """
    1) Grundumsatz (Harris-Benedict)
    2) Arbeitsumsatz (PAL)
    3) Workouts Kalorien (HEUTE)
    4) Tagesbedarf
    5) Ernährungsplanung (3 Hauptmahlzeiten + optional Snacks)
    6) Berücksichtigung von 1,5g Eiweiß / kg
    7) Ggf. Carbo-Periodisierung, grobe Hinweise
    """
    grundumsatz = berechne_grundumsatz_harris_benedict(
        user_data["geschlecht"],
        user_data["gewicht"],
        user_data["groesse"],
        user_data["alter"],
    )

    arbeitsumsatz = grundumsatz * user_data["pal"]

    kcal_workout_heute, kcal_workout_morgen = energie_verbrauch(
        user_data["training_heute"],
        user_data["training_morgen"],
        user_data["gewicht"],
        user_data["ftp"],
        user_data["zeit400m"]
    )

    tagesbedarf = arbeitsumsatz + kcal_workout_heute
    tagesbedarf = round(tagesbedarf, 2)

    # Proteinbedarf
    protein_bedarf = round(user_data["gewicht"] * 1.5, 2)

    # Kohlenhydrat-Strategie (stark vereinfacht)
    # Man könnte jetzt gucken, ob "GA" oder "HIT" => Dann mehr oder weniger KH
    # -> Hier nur ein generischer Hinweis.
    trainingsintensitaet = "unbekannt"
    if "hita" in user_data["training_heute"].lower() or "eb" in user_data["training_heute"].lower():
        trainingsintensitaet = "HIT"
    elif "ga" in user_data["training_heute"].lower():
        trainingsintensitaet = "GA"
    
    # Grobe Carbo-Regel: GA <-> Balanced, HIT <-> High-Carb
    if trainingsintensitaet == "HIT":
        kohlenhydrat_kategorie = "Rot (High-Carb)"
    else:
        kohlenhydrat_kategorie = "Gelb (Balanced)"

    # Beispiel-Mahlzeiten
    # Aufteilung: 25% / 35% / 25% + 15% für Snack
    kcal_frueh = round(tagesbedarf * 0.25)
    kcal_mittag = round(tagesbedarf * 0.35)
    kcal_snack = round(tagesbedarf * 0.15)
    kcal_abend = round(tagesbedarf * 0.25)

    plan_text = f"""
### Zusammenfassung deiner Werte
- **Grundumsatz** (Harris-Benedict): {grundumsatz} kcal
- **PAL-Faktor**: {user_data["pal"]}
- **Arbeitsumsatz**: {round(arbeitsumsatz, 2)} kcal
- **Kalorien für heutiges Training**: {kcal_workout_heute} kcal
- **Geschätzter Tagesbedarf**: {tagesbedarf} kcal
- **Proteinbedarf**: ca. {protein_bedarf} g/Tag (1,5 g/kg)

### Ernährungsstrategie (vereinfacht)
- Tages-Kalorienziel: {tagesbedarf} kcal
- Protein: mindestens {protein_bedarf} g
- Kohlenhydrat-Kategorie heute: {kohlenhydrat_kategorie}

### Mahlzeitenvorschlag
- **Frühstück** (~{kcal_frueh} kcal, {kohlenhydrat_kategorie}):
  - z.B. Haferflocken mit Milch oder Joghurt, Beeren, etwas Honig
  - Kaffee oder Tee
- **Mittagessen** (~{kcal_mittag} kcal, {kohlenhydrat_kategorie}):
  - z.B. Reis mit Hühnchen/Tofu, gedünstetes Gemüse
  - Wasser oder leichte Saftschorle
- **Snack** (~{kcal_snack} kcal, Grün/Balanced):
  - z.B. Handvoll Nüsse, Magerquark mit Früchten oder Protein-Shake
- **Abendessen** (~{kcal_abend} kcal, Gelb/Balanced):
  - z.B. Fisch oder mageres Fleisch mit Salat oder Gemüse
  - Bei spätem Training ggf. mehr KH einplanen

### Kohlenhydrate während des Trainings (aus deinem Guide)
- Grundlageneinheiten (GA) >60min: ab 45min ca. 30–45 g KH/Stunde
- Rad >90min: ab 2. Stunde 30–45 g KH/Stunde, ab 3. Stunde 60 g KH/Stunde
- Prep-Phase: 60–90 g KH/h (je nach Verträglichkeit)

### Recovery
- Nach harten Einheiten: 60 g KH + 30 g Protein (Whey/vegan) im Shake
- Auffüllen der Glykogenspeicher bei Back-to-Back Trainings

---
**Für morgen** hast du insgesamt ~{kcal_workout_morgen} kcal durch Training.
Passe deine abendliche KH-Menge ggf. etwas an, wenn es morgen früh intensiv wird.
    
---

**Wichtiger Hinweis**: Ein tägliches Kaloriendefizit sollte 500 kcal nicht dauerhaft überschreiten. Deine langfristige Gesundheit steht an erster Stelle!
    """
    return plan_text

# -----------------------------
# 5. Mahlzeitenvorschläge bestätigen & 6. Langfristige Nutzung
# (Hier nur Ansatz - man könnte PDF-Generierung integrieren)
# -----------------------------

def chat_antwort(user_input, plan_text):
    """
    Nimmt die Chat-Eingabe des Nutzers und reagiert darauf.
    - User kann nach Änderungen fragen
    - Oder den Plan bestätigen
    - Oder neu berechnen wollen
    """
    user_input_lower = user_input.lower()

    if "ändern" in user_input_lower or "änderung" in user_input_lower:
        return (
            "Kein Problem. Bitte sag mir, was du ändern möchtest, "
            "z.B. mehr Protein, weniger KH, andere Mahlzeiten?"
        )
    elif "bestätigen" in user_input_lower or "ok" in user_input_lower:
        return (
            "Alles klar! Ich erstelle dir gerne eine PDF mit den Rezepten und einer "
            "Einkaufsliste (diese Funktion müsstest du noch implementieren)."
        )
    elif "danke" in user_input_lower:
        return "Gern geschehen! Melde dich jederzeit, wenn du mehr brauchst."
    else:
        # Standard-Antwort: Plan nochmal anzeigen
        return (
            "Du kannst 'bestätigen' oder mir deine Änderungswünsche nennen.\n\n"
            "Hier nochmal dein aktueller Plan:\n\n"
            + plan_text
        )

# -----------------------------
# 7. Der komplette Streamlit-Ablauf
# -----------------------------
def main():
    st.set_page_config(page_title="NutriGPT", layout="centered")
    begruessung()

    if "user_data" not in st.session_state:
        st.session_state["user_data"] = {}
    if "plan" not in st.session_state:
        st.session_state["plan"] = ""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    st.header("2. Datenerfassung")

    with st.form("datenerfassung"):
        # Biometrische Daten
        geschlecht = st.selectbox("Geschlecht:", ["Männlich", "Weiblich"])
        alter = st.number_input("Alter (Jahre):", min_value=1, max_value=120, value=30)
        groesse = st.number_input("Größe (cm):", min_value=100, max_value=250, value=180)
        gewicht = st.number_input("Gewicht (kg):", min_value=30.0, max_value=250.0, value=70.0)
        koerperfett = st.number_input("Körperfettanteil (%):", min_value=0.0, max_value=60.0, value=15.0)

        st.write("### Ziele und Leistungswerte")
        ftp = st.number_input("FTP (Watt):", min_value=0, max_value=600, value=200)
        vo2max = st.number_input("VO2max (ml/min/kg):", min_value=0.0, max_value=90.0, value=50.0)
        vlamax = st.number_input("VLamax (mmol/l/s):", min_value=0.0, max_value=2.0, value=0.5)
        fatmax = st.number_input("Fatmax (kcal/h):", min_value=0.0, max_value=2000.0, value=300.0)
        zeit400m = st.number_input("Aktuelle 400m-Zeit (in min):", min_value=5.0, max_value=20.0, value=8.0)

        ziele = st.multiselect(
            "Was sind deine Ziele?",
            [
                "Volkstriathlon", "Olympische Distanz Triathlon", "Mitteldistanz Triathlon",
                "Langdistanz Triathlon", "Marathon", "Radmarathon", "Abnehmen",
                "Gewicht halten", "Muskelaufbau", "Leistungssteigerung",
                "Fettstoffwechsel verbessern", "VO2max steigern", "VLamax senken"
            ]
        )
        zeitlicher_rahmen = st.text_input("Zeitlicher Rahmen (z. B. Wettkampfdatum, Abnehmziel etc.)")

        st.write("### PAL-Wert (Physical Activity Level)")
        pal_wert = st.selectbox(
            "Bitte wähle deinen ungefähren PAL-Wert:",
            [
                "Sitzend (kaum Bewegung) ~1.2",
                "Sitzend (wenig Bewegung) ~1.4-1.5",
                "Überwiegend gehend/stehend ~1.6-1.7",
                "Körperlich anstrengende Arbeit ~1.8-2.2"
            ]
        )
        # Grobe Zuordnung
        if "1.2" in pal_wert:
            pal_num = 1.2
        elif "1.4" in pal_wert:
            pal_num = 1.45
        elif "1.6" in pal_wert:
            pal_num = 1.65
        else:
            pal_num = 1.9

        st.write("### Trainingseinheiten")
        training_heute = st.text_area(
            "Geplante Einheit(en) HEUTE (z. B. '60min Laufen GA1', mehrere Zeilen möglich):"
        )
        training_morgen = st.text_area(
            "Geplante Einheit(en) MORGEN (z. B. '90min Rad GA2', mehrere Zeilen möglich):"
        )

        submitted = st.form_submit_button("Daten übernehmen")
        if submitted:
            st.session_state["user_data"] = {
                "geschlecht": geschlecht,
                "alter": alter,
                "groesse": groesse,
                "gewicht": gewicht,
                "kfa": koerperfett,
                "ftp": ftp,
                "vo2max": vo2max,
                "vlamax": vlamax,
                "fatmax": fatmax,
                "zeit400m": zeit400m,
                "ziele": ziele,
                "zeitlicher_rahmen": zeitlicher_rahmen,
                "pal": pal_num,
                "training_heute": training_heute,
                "training_morgen": training_morgen
            }

            st.success("Deine Daten wurden übernommen. Scrolle weiter für deinen Ernährungsplan.")

    # Wenn Daten vorhanden sind, Ernährungsplan generieren
    if st.session_state["user_data"]:
        st.header("3. Trainingsplanung & 4. Ernährungsstrategie")
        if st.button("Ernährungsplan erstellen"):
            plan = erstelle_ernaehrungsplan(st.session_state["user_data"])
            st.session_state["plan"] = plan
            st.write(plan)

    # 5. Mahlzeitenvorschläge -> Sind im Plan integriert
    # 6. Chatfenster für Änderungswünsche
    st.header("Chat: Änderungswünsche oder Bestätigung")
    user_chat_input = st.text_input("Deine Nachricht an NutriGPT:")
    if st.button("Senden"):
        if not st.session_state["plan"]:
            st.warning("Bitte erst einen Ernährungsplan erstellen!")
        else:
            st.session_state["messages"].append({"role": "user", "content": user_chat_input})
            response = chat_antwort(user_chat_input, st.session_state["plan"])
            st.session_state["messages"].append({"role": "assistant", "content": response})

    # Chat-Verlauf anzeigen
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"**Du**: {msg['content']}")
        else:
            st.markdown(f"**NutriGPT**: {msg['content']}")

    st.write("---")
    st.write("**Hinweis zur Langfristigkeit**: Deine Daten können für zukünftige Interaktionen gespeichert werden, "
             "um Pläne dynamisch anzupassen. Achte darauf, bei jeder neuen Nutzung anzugeben, "
             "ob sich Gewicht oder KFA geändert haben.")
    st.write("*Das tägliche Kaloriendefizit sollte 500 kcal nicht dauerhaft überschreiten. Gesundheit geht vor!*")

if __name__ == "__main__":
    main()
