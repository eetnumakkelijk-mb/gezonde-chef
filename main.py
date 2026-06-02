import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Gezonde Restjes Chef Pro", layout="centered")

# INITIALISATIE: We houden het aantal gratis pogingen bij (Nu maximaal 2!)
if "teller" not in st.session_state:
    st.session_state.teller = 0
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

st.title("🥗 Gezonde Restjes Chef")
st.subheader("Voer je restjes in en de AI-Chef bedenkt een super gezond recept!")

# VERDIENMODEL DISPLAY: Laat de gebruiker zien hoeveel credits hij nog heeft
if not st.session_state.is_premium:
    credits_over = max(0, 2 - st.session_state.teller)
    st.info(f"💡 Je hebt nog **{credits_over} gratis** gezonde recept-credits over.")
else:
    st.success("✨ Pro Status: Actief (Onbeperkt gezonde recepten genereren)")

# GEBRUIKERSGEMAK: Super duidelijke instructie voor meerdere ingrediënten
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

# API sleutel (Voor gebruik op je eigen computer of via Streamlit secrets)
api_key = st.text_input("Voer je OpenAI API sleutel in:", type="password")

st.markdown("---")

# DE BETAALMUUR LOGICA (Blokkeert na exact 2 recepten)
if st.session_state.teller >= 2 and not st.session_state.is_premium:
    st.error("🛑 Je gratis credits zijn op!")
    st.markdown("""
    ### Ontgrendel Onbeperkt Gezond Koken!
    Je hebt je 2 gratis gezonde recepten gebruikt. Koop de **Pro Versie** om direct toegang te krijgen tot:
    * 🚀 Onbeperkt gezonde recepten genereren
    * 🥑 Uitgebreide gezondheidsstatistieken (Macro's en calorieën per maaltijd)
    * ❌ Geen limieten meer: voorkom voedselverspilling én eet elke dag gezond!
    """)
    
    # JOUW STRIPE BETAALKNOP (Vervang deze link straks door je eigen Stripe-link)
    st.link_button("💳 Ontgrendel Pro voor €2,99", "https://stripe.com")
    
    st.markdown("---")
    # Knop voor jou om te testen hoe het eruit ziet na betaling
    if st.button("Simuleer Succesvolle Betaling (Admin Test Knop)"):
        st.session_state.is_premium = True
        st.rerun()

else:
    # DE GENERATOR KNOP (Alleen actief als er credits zijn of als er betaald is)
    if st.button("Genereer Mijn Gezonde Recept 🥦"):
        if not api_key:
            st.error("Voer eerst je OpenAI API sleutel in.")
        elif not ingredienten:
            st.warning("Vul eerst je ingrediënten in! Voeg meerdere producten toe gescheiden door een komma.")
        else:
            with st.spinner("De chef-kok berekent de meest gezonde combinatie... 🧑‍🍳"):
                try:
                    client = OpenAI(api_key=api_key)
                    # DE PROMPT IS GEOPTIMALISEERD VOOR GEZONDHEID & BENADRUKKING HIERVAN
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
                            {"role": "system", "content": "Je bent een professionele restjes-chef en voedingsdeskundige. Je focust altijd op maximale gezondheid, vitaminen en gezonde voedingsstoffen. Antwoord altijd in het Nederlands."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    recept = response.choices.message.content
                    st.success("Smakelijk eten! Hier is je persoonlijke en gezonde recept:")
                    st.markdown(recept)
                    
                    # Verhoog de teller na een succesvol recept
                    st.session_state.teller += 1
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Fout bij het ophalen van het recept: {e}")
