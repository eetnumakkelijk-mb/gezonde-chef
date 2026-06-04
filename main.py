import streamlit as st
from openai import OpenAI
from datetime import datetime

st.set_page_config(page_title="Gezonde Restjes Chef", layout="centered")

st.title("🥗 Gezonde Restjes Chef")
st.subheader("Voer je restjes in en kook gezond!")

# INITIALISATIE: We tellen het aantal gegenereerde recepten
if "teller" not in st.session_state:
    st.session_state.teller = 0
if "donatie_gesloten_maand" not in st.session_state:
    st.session_state.donatie_gesloten_maand = ""

huidige_maand = datetime.now().strftime("%B %Y")

# SLIMME DONATIE-KAART: Verschijnt pas NA 5 recepten
if st.session_state.teller >= 5 and st.session_state.donatie_gesloten_maand != huidige_maand:
    st.info(f"❤️ **Maandelijkse Donatie Oproep ({huidige_maand}):**  \n"
            "Je hebt deze maand al meer dan 5 gezonde recepten gegenereerd! Omdat de AI geld kost, "
            "vraag ik actieve gebruikers om een kleine donatie te doen om deze app gratis en zonder reclame online te houden. "
            "Kies een bedrag dat bij je past:")
    
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
ingredienten = st.text_area("Typ alle ingrediënten, gescheiden door een komma:", placeholder="Bijv. kip, broccoli, eieren, ui")
extra_wensen = st.text_input("Extra wensen? (Optioneel)", placeholder="Bijv. binnen 15 minuten, koolhydraatarm")

st.markdown("---")

# DE GENERATOR KNOP
if st.button("🧑‍🍳 Bedenk Mijn Gezonde Recept!"):
    if not ingredienten:
        st.warning("Vul eerst je ingrediënten in!")
    else:
        with st.spinner("De chef-kok denkt na... 🍲"):
            try:
                api_key = st.secrets["OPENAI_API_KEY"]
                client = OpenAI(api_key=api_key)
                
                prompt = f"Bedenk een zo gezond mogelijk recept met: {ingredienten}. Wensen: {extra_wensen}. Leg uit waarom het gezond is."
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Je bent een gezonde chef. Antwoord in het Nederlands."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                recept = response.choices.pop(0).message.content
                st.success("Smakelijk eten!")
                st.markdown(recept)
                
                st.session_state.teller += 1
                st.rerun()
                
            except Exception as e:
                st.error(f"Fout: {e}")
