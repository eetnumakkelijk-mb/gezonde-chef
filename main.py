import streamlit as st  
from openai import OpenAI  
st.set_page_config(page_title="Gezonde Restjes Chef Pro", layout="centered")  
if "teller" not in st.session_state: st.session_state.teller = 0  
if "is_premium" not in st.session_state: st.session_state.is_premium = False  
st.title("🧑‍🍳 Gezonde Restjes Chef")  
st.subheader("Voer je restjes in!")  
if not st.session_state.is_premium: st.info(f"Je hebt nog {max(0, 2 - st.session_state.teller)} gratis credits.")  
else: st.success("Pro Status: Actief")  
ingredienten = st.text_area("Typ alle ingredienten, gescheiden door een komma:", placeholder="Bijv. kip, broccoli, rijst")  
extra_wensen = st.text_input("Extra wensen?", placeholder="Bijv. binnen 15 minuten")  
api_key = st.secrets["OPENAI_API_KEY"]  
if st.session_state.teller  and not st.session_state.is_premium:  
    st.error("Je gratis credits zijn op!")  
    st.link_button("Ontgrendel Pro voor 2,99", "https://stripe.com")  
    if st.button("Simuleer Succesvolle Betaling"):  
        st.session_state.is_premium = True  
        st.rerun()  
else:  
    if st.button("🥦Genereer Mijn Gezonde Recept"):  
        if not ingredienten: st.warning("Vul eerst je ingredienten in!")  
        else:  
            with st.spinner("De chef denkt na..."):  
                try:  
                    client = OpenAI(api_key=api_key); prompt = f"Bedenk een gezond recept met: {ingredienten}. Wensen: {extra_wensen}. Leg uit waarom het gezond is."; response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": "Je bent een gezonde chef. Antwoord in het Nederlands."}, {"role": "user", "content": prompt}]);  
                    recept = response.choices[0].message.content; st.success("Smakelijk eten!"); st.markdown(recept); st.session_state.teller += 1; st.rerun()  
                except Exception as e: st.error(f"Fout: {e}") 
