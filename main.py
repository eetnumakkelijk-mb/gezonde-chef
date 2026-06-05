import streamlit as st
from openai import OpenAI
from datetime import datetime
import os

# AUTOMATISCHE KLEURENMAKER: Olijfgeel, zachtgroene vlakken en kookboeklettertype
if not os.path.exists(".streamlit"):
    os.makedirs(".streamlit")
with open(".streamlit/config.toml", "w") as f:
    f.write("[theme]\nprimaryColor = '#557a5e'\nbackgroundColor = '#f4f5e9'\nsecondaryBackgroundColor = '#e9ebd7'\ntextColor = '#213326'\nfont = 'serif'\n")

# 1. STRUCTUUR VAN DE APP (100% VEILIG VOOR PYTHON 3.14)
st.set_page_config(page_title="Gezonde Restjes Chef", layout="centered")

# 2. SFEERVOLLE VISUELE INTRODUCTIE
st.write("---")
st.markdown("## 🧑‍🍳 📔 JOUW PERSOONLIJKE RECEPTENBOEK")
st.markdown("### 🥦 🌽 🍅 *Vers van de groenteafdeling in jouw keuken!* 🌶️ 🧅 🍋")
st.write("---")

st.success("""
    ✨ **Welkom in de gezellige keuken!** 👋
    
    Jouw persoonlijke **Restjes Chef** helpt je om heerlijk en gezond te koken. 
    Kies hieronder of je wilt koken met restjes uit je koelkast, of dat je samen met de chef een gloednieuw gezond gerecht wilt samenstellen!
""")

# INITIALISATIE: We tellen het aantal gegenereerde recepten
if "teller" not in st.session_state:
    st.session_state.teller = 0
if "donatie_gesloten_maand" not in st.session_state:
    st.session_state.donatie_gesloten_maand = ""

huidige_maand = datetime.now().strftime("%B %Y")

# SLIMME DONATIE-KAART: Verschijnt pas NA 5 recepten
if st.session_state.teller >= 5 and st.session_state.donatie_gesloten_maand != huidige_maand:
    st.warning(f"❤️ **Maandelijkse Donatie Oproep ({huidige_maand}):**  \n"
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
        st.session_state.donatie_gesloten_maand = huidige_maand
        st.rerun()

st.markdown("---")

# 3. KIES JE KOOKSTIJL (TABBLADEN)
tab1, tab2 = st.tabs(["🗑️ Koken met Restjes", "✨ Nieuw Gerecht Samenstellen"])

with tab1:
    st.markdown("### 🥑 1. Wat ligt er nog in je koelkast?")
    st.markdown("**Typ alle ingrediënten die je op wilt maken, gescheiden door een komma:**")
    ingredienten = st.text_area(
        label="Restjes invoer",
        label_visibility="collapsed",
        placeholder="Bijv. kip, broccoli, eieren, oude kaas, ui, tomaat...",
        key="restjes_invoer"
    )
    
    st.markdown("### 🍲 2. Extra wensen? (Optioneel)")
    extra_wensen_1 = st.text_input(
        label="Wensen restjes",
        label_visibility="collapsed",
        placeholder="Bijv. binnen 15 minuten, vegetarisch, koolhydraatarm",
        key="wensen_restjes"
    )
    mode = "restjes"

with tab2:
    st.markdown("### 🍝 1. Kies je basis voor het nieuwe gerecht")
    basis_keuze = st.selectbox(
        "Wat voor soort maaltijd wil je maken?",
        ["Gezonde Volkoren Pasta", "Zilvervliesrijst / Quinoa Schotel", "Gevulde Volkoren Wrap", "Frisse Maaltijdsalade", "Warme Ovenschotel", "Slanke Soep / Stoofpot"]
    )
    
    st.markdown("### 🥩 🥕 2. Voeg extra ingrediënten toe die je lekker vindt")
    st.markdown("**Typ hier wat je er sowieso in wilt hebben (gescheiden door een komma):**")
    extra_ingredienten = st.text_area(
        label="Nieuw gerecht invoer",
        label_visibility="collapsed",
        placeholder="Bijv. zalm, spinazie, courgette, feta, avocado, pijnboompitten...",
        key="nieuw_invoer"
    )
    
    st.markdown("### 🍋 3. Extra wensen? (Optioneel)")
    extra_wensen_2 = st.text_input(
        label="Wensen nieuw",
        label_visibility="collapsed",
        placeholder="Bijv. extra eiwit, pittig, kindvriendelijk",
        key="wensen_nieuw"
    )
    mode = "nieuw"

st.markdown("---")

# 4. DE GENERATOR KNOP
st.markdown("### 🍳 🌿 🍲 🌶️ 👨‍🍳 Recept samenstellen")
if st.button("🔥 Heb je alles ingevuld? Klik dan hier voor je recept! 🍳 🔥", use_container_width=True, type="primary"):
    
    # Bepaal de prompt op basis van de gekozen tab
    if mode == "restjes":
        if not ingredienten:
            st.warning("Vul eerst de restjes uit je koelkast in!")
            st.stop()
        prompt = (
            f"Bedenk als de persoonlijke 'Restjes Chef' een zo gezond mogelijk en logisch recept met deze koelkast-restjes: {ingredienten}. "
            f"Extra wensen: {extra_wensen_1}. "
            f"Het hoofddoel is voedselverspilling tegengaan. Geef het recept een duidelijke titel, bereidingstijd, ingrediëntenlijst met hoeveelheden en een stappenplan. "
            f"Voeg aan het begin een alinea toe met de titel 'Waarom dit gerecht super gezond is:'."
        )
    else:
        prompt = (
            f"Bedenk als de persoonlijke 'Restjes Chef' een gloednieuw, zo gezond mogelijk recept met als basis '{basis_keuze}'. "
            f"Voeg de volgende favoriete ingrediënten toe: {extra_ingredienten if extra_ingredienten else 'Chef kiest bijpassende gezonde groenten'}. "
            f"Extra wensen: {extra_wensen_2}. "
            f"Geef het recept een duidelijke titel, bereidingstijd, ingrediëntenlijst met hoeveelheden en een stappenplan. "
            f"Voeg aan het begin een alinea toe met de titel 'Waarom dit gerecht super gezond is:'."
        )

    with st.spinner("De Restjes Chef berekent de meest gezonde combinatie... 🍲"):
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
            client = OpenAI(api_key=api_key)
            
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
            
        except Exception as e:
            st.error(f"Fout bij het ophalen van het recept: {e}")
