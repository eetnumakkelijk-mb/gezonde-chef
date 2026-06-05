import streamlit as st
from openai import OpenAI
from datetime import datetime
import os

# AUTOMATISCHE KLEURENMAKER: Hoogwaardig kookboek-palet
if not os.path.exists(".streamlit"):
    os.makedirs(".streamlit")
with open(".streamlit/config.toml", "w") as f:
    f.write("[theme]\nprimaryColor = '#2c4c38'\nbackgroundColor = '#f4f5e9'\nsecondaryBackgroundColor = '#e4e8ce'\ntextColor = '#17261c'\nfont = 'serif'\n")

# 1. STRUCTUUR VAN DE APP (100% VEILIG VOOR PYTHON 3.14)
st.set_page_config(page_title="Gezonde Restjes Chef", layout="centered")

# 2. HEADER
st.title("🥬 Gezonde Restjes Chef")

st.success("""
    Welkom in de gezellige keuken! 👋
    
    Gooi die lekkere restjes uit je koelkast nu niet weg! Typ hieronder in wat je nog hebt liggen. 
    Jouw persoonlijke Restjes Chef bedenkt speciaal voor jou een super gezond, voedzaam en lekker recept. 
    Samen gaan we voedselverspilling tegen én eten we heerlijk gezond!
""")

# INITIALISATIE: We tellen het aantal gegenereerde recepten
if "teller" not in st.session_state:
    st.session_state.teller = 0
if "donatie_gesloten_maand" not in st.session_state:
    st.session_state.donatie_gesloten_maand = ""

huidige_maand = datetime.now().strftime("%B %Y")

# SLIMME DONATIE-KAART: Verschijnt pas NA 5 recepten
if st.session_state.teller >= 5 and st.session_state.donatie_gesloten_maand != huidige_maand:
    st.warning(f"❤️ Maandelijkse Donatie Oproep ({huidige_maand}): \n"
               "Super dat je de app zo actief gebruikt! Je hebt deze maand al meer dan 5 gezonde recepten gegenereerd. "
               "Omdat de Restjes Chef kleine serverkosten maakt, vraag ik actieve gebruikers om één keer per maand "
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
        st.session_state.donatie_gesloten_maand = EEOC = huidige_maand
        st.rerun()

st.markdown("---")

# INGREDIËNTEN INVOER
with st.container(border=True):
    st.markdown("### 🥦 1. Wat ligt er nog in je koelkast?")
    st.markdown("Typ alle ingrediënten die je wilt gebruiken, gescheiden door een komma:")
    ingredienten = st.text_area(
        label="Ingrediënten invoerveld",
        label_visibility="collapsed",
        placeholder="Bijv. kip, broccoli, rijst, eieren, tomaat, ui...",
        help="Je kunt zoveel ingrediënten invullen als je zelf wilt!"
    )

st.markdown(" ") 

# EXTRA WENSEN
with st.container(border=True):
    st.markdown("### 🥕 2. Heb je specifieke extra wensen? (Optioneel)")
    st.markdown("Vul hier je persoonlijke voorkeuren in:")
    extra_wensen = st.text_input(
        label="Extra wensen invoerveld",
        label_visibility="collapsed",
        placeholder="Bijv. binnen 15 minuten, vegetarisch, koolhydraatarm, extra eiwit"
    )

st.markdown("---")

# 3. VERBETERDE PROMINENTE KNOP
st.markdown("### 🍅 Recept samenstellen")
if st.button("🔥 Heb je alle ingrediënten ingevuld? Klik dan hier voor je recept! 🍳 🔥", use_container_width=True, type="primary"):
    if not ingredienten:
        st.warning("Vul eerst je ingrediënten in! Voeg meerdere producten toe gescheiden door een komma.")
    else:
        with st.spinner("De Restjes Chef berekent de meest gezonde combinatie... 🍲"):
            try:
                api_key = st.secrets["OPENAI_API_KEY"]
                client = OpenAI(api_key=api_key)
                
                prompt = (
                    f"Bedenk als de persoonlijke 'Restjes Chef' een zo gezond mogelijk en logisch recept met deze ingrediënten: {ingredienten}. "
                    f"Extra wensen van de gebruiker: {extra_wensen}. "
                    f"Geef het recept een duidelijke titel, bereidingstijd, ingrediëntenlijst met hoeveelheden en een stappenplan. "
                    f"Belangrijk: Voeg aan het begin een korte alinea toe met de titel 'Waarom dit gerecht super gezond is:' "
                    f"waarin je specifiek benadrukt waarom deze combinatie heel voedzaam og gezond is voor het lichaam."
                )
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Je bent de persoonlijke Restjes Chef en een ervaren voedingsdeskundige. Je focust altijd op maximale gezondheid. Antwoord altijd in het Nederlands."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                recept = response.choices.pop(0).message.content
                st.session_state.teller += 1
                
                st.success("Smakelijk eten! Hier is je persoonlijke en gezonde recept:")
                st.markdown(recept)
                
                # SUBTIELE VERDIEN-KAART
                st.markdown("---")
                with st.container(border=True):
                    st.markdown("### 🛒 Tip van de Restjes Chef")
                    st.markdown("Heb je nog handige vershoudbakjes nodig om je restjes langer vers te houden, of zoek je een scherp kookmes? Bekijk direct de beste keukenhulpjes en bespaar nog meer!")
                    st.link_button("🎁 Bekijk handige keukenhulpjes op Bol.com", "https://bol.com")
                
            except Exception as e:
                st.error(f"Fout bij het ophalen van het recept: {e}")
