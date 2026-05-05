import streamlit as st
import random

# Rozbudowana baza danych z obraz.png
DANE_SLOWKA = {
    "Exceptional": "wyjątkowy", "Stunning": "zachwycający", "Hideous": "paskudny",
    "Appalling": "przerażający/beznadziejny", "Vast": "ogromny", "Minute": "malutki",
    "Essential": "niezbędny", "Crucial": "kluczowy", "Tedious": "nużący",
    "Hilarious": "komiczny", "Thrilled": "podekscytowany", "Miserable": "nieszczęśliwy",
    "Vivid": "obrazowy/wyrazisty", "Straightforward": "jasny/prosty", "Obscure": "niejasny/mało znany",
    "To enhance": "ulepszać/wzmacniać", "To diminish": "zmniejszać się", "To maintain": "utrzymywać",
    "To acquire": "nabywać", "To obtain": "uzyskiwać", "To clarify": "wyjaśniać",
    "Furthermore": "ponadto", "Moreover": "co więcej", "Nevertheless": "niemniej jednak",
    "Consequently": "w rezultacie", "Thus": "zatem", "Alternatively": "ewentualnie",
    "Advantage": "zaleta", "Drawback": "wada", "Benefit": "korzyść",
    "Consequence": "konsekwencja", "Opportunity": "okazja/możliwość", "Solution": "rozwiązanie",
    "Cope with": "radzić sobie z", "Account for": "wyjaśniać/stanowić część", "Break through": "przełamać się"
}

st.set_page_config(page_title="Fiszki Angielski", page_icon="🇬🇧")

# Inicjalizacja stanu aplikacji
if 'pytanie' not in st.session_state:
    st.session_state.wynik = 0
    st.session_state.proby = 0

def losuj_nowe_pytanie():
    slowo = random.choice(list(DANE_SLOWKA.keys()))
    poprawna = DANE_SLOWKA[slowo]
    
    # Losowanie 3 błędnych odpowiedzi
    inne = [v for v in DANE_SLOWKA.values() if v != poprawna]
    bledne = random.sample(inne, 3)
    
    opcje = bledne + [poprawna]
    random.shuffle(opcje)
    
    st.session_state.pytanie = slowo
    st.session_state.poprawna = poprawna
    st.session_state.opcje = opcje
    st.session_state.odpowiedziano = False

# Pierwsze losowanie
if 'pytanie' not in st.session_state:
    losuj_nowe_pytanie()

st.title("🇬🇧 Fiszki z obraz.png")
st.write(f"Twój wynik: **{st.session_state.wynik}** / {st.session_state.proby}")

# Wyświetlanie pytania
st.subheader(f"Słowo: `{st.session_state.pytanie}`")

# Formularz z opcjami
with st.form(key='quiz_form'):
    wybor = st.radio("Wybierz poprawne tłumaczenie:", st.session_state.opcje, index=None)
    submit = st.form_submit_button("Sprawdź!")

if submit:
    if wybor is None:
        st.warning("Musisz coś wybrać!")
    else:
        st.session_state.proby += 1
        if wybor == st.session_state.poprawna:
            st.success("✅ Świetnie! To poprawna odpowiedź.")
            st.session_state.wynik += 1
            st.balloons()
        else:
            st.error(f"❌ Błąd. Poprawna odpowiedź to: **{st.session_state.poprawna}**")
        
        st.button("Następne pytanie ➡️", on_click=losuj_nowe_pytanie)

# Przycisk restartu (opcjonalny)
if st.sidebar.button("Zresetuj wynik"):
    st.session_state.wynik = 0
    st.session_state.proby = 0
    losuj_nowe_pytanie()
    st.rerun()
