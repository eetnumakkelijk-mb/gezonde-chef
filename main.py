import streamlit as st
from openai import OpenAI
from datetime import datetime

st.set_page_config(page_title="Gezonde Restjes Chef", layout="centered")

st.title("🥗 Gezonde Restjes Chef")
st.subheader("Voer je restjes in en de AI-Chef bedenkt een super gezond recept!")

# VRIJBLIJVENDE DONATIE OPROEP (1x per maand herinnering)
huidige_maand = datetime.now().strftime("%B %Y")
st.info(f"❤️ **Maandelijkse Donatie Oproep ({huidige_maand}):**  \n"
        "Vind je deze gezonde recepten waardevol? De AI-chef kost per klik een kleine bijdrage. "
        "Om deze app volledig gratis, zonder reclame en als hobby online te houden, "
        "vraag ik gebruikers om één keer per maand een vrijblijvende donatie te doen ter waarde van een kopje koffie. "
        "Super bedankt voor je steun! 🙏")

st.markdown("---")

# INGREDIËNTEN INVOER
st.markdown("### 1. Voer je ingrediënten in")
ingredienten = st.text_area(
    "Typ alle ingrediënten die je wilt gebruiken, gescheiden door een komma:",
    placeholder="Bijv. kip, broccoli, rijst, eieren, oude kaas, ui, tomaat",
    help="Je kunt zoveel ingrediënten invullen als je zelf wilt! Hoe meer je invult, hoe beter het recept."
)

st.markdown("### 2. Extra wensen (Optioneel)")
extra_wensen = st.text_input(
    "Heb je specifieke voorkeuren?", 
    placeholder="Bijv. binnen 15 minuten, vegetarisch, koolhydraatarm, extra eiwit"
)

st.markdown("---")

# DE GENERATOR KNOP
if st.button("Genereer Mijn Gezonde Recept 🥦"):
    if not ingredienten:
        st.warning("Vul eerst je ingrediënten in! Voeg meerdere producten toe gescheiden door een komma.")
    else:
        with st.spinner("De chef-kok berekent de meest gezonde combinatie... 🧑‍🍳"):
            try:
                # Haal de sleutel onzichtbaar op uit de Streamlit Secrets
                api_key = st.secrets["OPENAI_API_KEY"]
                client = OpenAI(api_key=api_key)
                
                prompt = (
                    f"Bedenk een zo gezond mogelijk en logisch recept met deze ingrediënten: {ingredienten}. "
                    f"Extra wensen van de gebruiker: {extra_wensen}. "
                    f"Geef het recept een duidelijke titel, bereidingstijd, ingrediëntenlijst met hoeveelheden en een stappenplan. "
                    f"Belangrijk: Voeg aan het begin een korte alinea toe met de titel 'Waarom dit gerecht super gezond is:' "
                    f"waarin je specifiek benadrukt waarom deze combinatie heel voedzaam en gezond is voor het lichaam."
                )
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Je bent een professionele restjes-chef en voedingsdeskundige. Je focust altijd op maximale gezondheid. Antwoord altijd in het Nederlands."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # DE CRUCIALE REPARATIE HIER (met de pop-functie zodat het chatvenster niks filtert):
                recept = response.choices.pop(0).message.content
                
                st.success("Smakelijk eten! Hier is je persoonlijke en gezonde recept:")
                st.markdown(recept)
                
            except Exception as e:
                st.error(f"Fout bij het ophalen van het recept: {e}")
