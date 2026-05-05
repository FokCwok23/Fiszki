import streamlit as st
import random

# Dane z obraz.png
slowka = {
    "Exceptional": "wyjątkowy",
    "Stunning": "zachwycający",
    "Hideous": "paskudny",
    "Appalling": "przerażający/beznadziejny",
    "Vast": "ogromny",
    "Minute": "malutki",
    "Essential": "niezbędny",
    "Crucial": "kluczowy"
    # ... tutaj dodaj resztę słówek
}

st.title("🗂️ Moje Fiszki Angielskiego")

# Inicjalizacja stanu sesji (żeby aplikacja "pamiętała" słowo po kliknięciu)
if 'pytanie' not in st.session_state:
    st.session_state.pytanie = random.choice(list(slowka.keys()))
    poprawna = slowka[st.session_state.pytanie]
    inne = [v for k, v in slowka.items() if v != poprawna]
    opcje = random.sample(inne, 3) + [poprawna]
    random.shuffle(opcje)
    st.session_state.opcje = opcje

def nastepne_pytanie():
    st.session_state.pytanie = random.choice(list(slowka.keys()))
    poprawna = slowka[st.session_state.pytanie]
    inne = [v for k, v in slowka.items() if v != poprawna]
    st.session_state.opcje = random.sample(inne, 3) + [poprawna]
    random.shuffle(st.session_state.opcje)

st.subheader(f"Jak przetłumaczysz: **{st.session_state.pytanie}**?")

# Przyciski z opcjami
for opcja in st.session_state.opcje:
    if st.button(opcja, use_container_width=True):
        if opcja == slowka[st.session_state.pytanie]:
            st.success("✅ Brawo! To poprawna odpowiedź.")
            st.balloons()
        else:
            st.error(f"❌ Nie. Poprawna odpowiedź to: {slowka[st.session_state.pytanie]}")
        
        st.button("Następne słówko ➡️", on_click=nastepne_pytanie)
