import streamlit as st
from openai import OpenAI
from datetime import datetime

# 1. WARME KLAREN EN STYLING INBOUWEN
st.set_page_config(page_title="Gezonde Restjes Chef", layout="centered")

# Custom CSS voor een warme, culinaire sfeer (Zachtgroen/crème tinten)
st.markdown("""
    <style>
        /* Achtergrond van de hele app warm maken */
        .stApp {
            background-color: #f7f9f6;
        }
        /* Alle grote titels een diepe, warme groen/bruine kleur geven */
        h1, h2, h3 {
            color: #2c4c38 !important;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        /* Tekstvakken een zachte rand geven */
        .stTextArea textarea, .stTextInput input {
            border: 1px solid #c2d1c6 !important;
            background-color: #ffffff !important;
        }
    </style>
""", unsafe_with_html=True)

# 2. SFEERVOLLE HEADER
st.title("🧑‍🍳 Gezonde Restjes Chef")

# We plaatsen de introductie in een warme, gezellige welkomstkaart
st.markdown("""
    <div style="background-color: #e8f0ea; padding: 20px; border-radius: 12px; margin-bottom: 25px; border-left: 5px solid #4a7c59;">
        <h4 style="margin-0; color: #2c4c38; font-weight: bold;">Welkom in de keuken! 👋</h4>
        <p style="margin: 5px 0 0 0; color: #3d5a45; font-size: 15px;">
            Gooi die lekkere restjes uit je koelkast niet weg! Typ hieronder in wat je nog hebt liggen. 
            Mijn slimme AI-Chef bedenkt speciaal voor jou een super gezond, voedzaam en logisch recept. 
            Samen gaan we voedselverspilling tegen én eten we heerlijk gezond!
        </p>
    </div>
""", unsafe_with_html=True)

# INITIALISATIE: We tellen het aantal gegenereerde recepten
if "teller" not in st.session_state:
    st.session_state.teller = 0
if "donatie_gesloten_maand" not in st.session_state:
    st.session_state.donatie_gesloten_maand = ""

huidige_maand = datetime.now().strftime("%B %Y")

# SLIMME DONATIE-KAART: Verschijnt pas NA 5 recepten
if st.session_state.teller >= 5 and st.session_state.donatie_gesloten_maand != huidige_maand:
    st.info(f"❤️ **Maandelijkse Donatie Oproep ({huidige_maand}):**  \n"
            "Super dat je de app zo actief gebruikt! Je hebt deze maand al meer dan 5 gezonde recepten gegenereerd. "
            "Omdat de AI-chef per klik geld kost, vraag ik actieve gebruikers om één keer per maand "
            "een vrijblijvende donatie te doen om deze app gratis en zonder reclame online te houden. "
            "Kies hieronder een bedrag dat bij je past. Super bedankt voor je steun! 🙏")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button("☕ Doneer € 1,50", "https://buymeacoffee.com")
    with col2:
        st.link_button("🍕 Doneer € 2,50", "https://buymeacoffee.com")
    with col3:
        st.link_button("👑 Doneer € 3,00", "https://buymeacoffee.com")
    
    st.markdown(" ") 
    if st.button("❌ Gelezen, sluit melding voor deze maand"):
        st.session_state.donatie_gesloten_maand = huidige_maand
        st.rerun()

st.markdown("---")

# INGREDIËNTEN INVOER
st.markdown("### 🥑 1. Wat ligt er nog in je koelkast?")
ingredienten = st.text_area(
    "Typ alle ingrediënten die je wilt gebruiken, gescheiden door een komma:",
    placeholder="Bijv. kip, broccoli, rijst, eieren, tomaat, ui...",
    help="Je kunt zoveel ingrediënten invullen als je zelf wilt!"
)

st.markdown("### 📝 2. Extra wensen (Optioneel)")
extra_wensen = st.text_input(
    "Heb je specifieke voorkeuren?", 
    placeholder="Bijv. binnen 15 minuten, vegetarisch, koolhydraatarm, extra eiwit"
)

st.markdown("---")

# DE GENERATOR KNOP
if st.button("🧑‍🍳 Bedenk Mijn Gezonde Recept!"):
    if not ingredienten:
        st.warning("Vul eerst je ingrediënten in! Voeg meerdere producten toe gescheiden door een komma.")
    else:
        with st.spinner("De chef-kok berekent de meest gezonde combinatie... 🍲"):
            try:
                api_key = st.secrets["OPENAI_API_KEY"]
                client = OpenAI(api_key=api_key)
                
                prompt = (
                    f"Bedenk een zo gezond mogelijk en logisch recept met deze ingrediënten: {ingredienten}. "
                    f"Extra wensen van de gebruiker: {extra_wensen}. "
                    f"Geef het recept een duidelijke titel, bereidingstijd, ingrediëntenlijst met hoeveelheden en een stappenplan. "
                    f"Belangrijk: Voeg aan het begin een korte alinea toe met de titel 'Waarom dit gerecht super gezond is:' "
                    f"waarin je specifiek benadrukt waarom deze combinatie heel voedzaam og gezond is voor het lichaam."
                )
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Je bent een professionele restjes-chef en voedingsdeskundige. Je focust altijd op maximale gezondheid. Antwoord altijd in het Nederlands."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                recept = response.choices.pop(0).message.content
                
                st.success("Smakelijk eten! Hier is je persoonlijke en gezonde recept:")
                st.markdown(recept)
                
                st.session_state.teller += 1
                st.rerun()
                
            except Exception as e:
                st.error(f"Fout bij het ophalen van het recept: {e}")
