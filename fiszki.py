import streamlit as st
import random

# Dane z obraz.png
DANE_SLOWKA = {
    "Exceptional": "wyjątkowy", "Stunning": "zachwycający", "Hideous": "paskudny",
    "Appalling": "przerażający/beznadziejny", "Vast": "ogromny", "Minute": "malutki",
    "Essential": "niezbędny", "Crucial": "kluczowy", "Tedious": "nużący",
    "Hilarious": "komiczny", "Thrilled": "podekscytowany", "Miserable": "nieszczęśliwy",
    "Vivid": "obrazowy/wyrazisty", "Straightforward": "jasny/prosty", "Obscure": "niejasny/mało znany",
    "To enhance": "ulepszać/wzmacniać", "To diminish": "zmniejszać się", "To maintain": "utrzymywać",
    "To acquire": "nabywać", "To obtain": "uzyskiwać", "Furthermore": "ponadto",
    "Moreover": "co więcej", "Nevertheless": "niemniej jednak", "Consequently": "w rezultacie"
}

st.set_page_config(page_title="Fiszki Master", layout="wide")

# --- LOGIKA SESJI ---
if 'zaliczone' not in st.session_state:
    st.session_state.zaliczone = set()
if 'niezaliczone' not in st.session_state:
    st.session_state.niezaliczone = set()
if 'aktualne_pytanie' not in st.session_state:
    st.session_state.aktualne_pytanie = None

def losuj_slowo():
    # Losujemy spośród tych, które nie są jeszcze "zaliczone"
    dostepne = [s for s in DANE_SLOWKA.keys() if s not in st.session_state.zaliczone]
    if not dostepne:
        return None
    
    slowo = random.choice(dostepne)
    poprawna = DANE_SLOWKA[slowo]
    inne = [v for v in DANE_SLOWKA.values() if v != poprawna]
    opcje = random.sample(inne, 3) + [poprawna]
    random.shuffle(opcje)
    
    return {"slowo": slowo, "poprawna": poprawna, "opcje": opcje}

if st.session_state.aktualne_pytanie is None:
    st.session_state.aktualne_pytanie = losuj_slowo()

# --- PASEK BOCZNY (SIDEBAR) ---
with st.sidebar:
    st.header("📊 Twój Postęp")
    
    # Statystyki
    col1, col2 = st.columns(2)
    col1.metric("Zaliczone", len(st.session_state.zaliczone))
    col2.metric("Błędy", len(st.session_state.niezaliczone))
    
    st.write("---")
    
    # Lista słówek
    st.subheader("✅ Zaliczone")
    for s in sorted(st.session_state.zaliczone):
        st.write(f"✔️ {s}")
        
    st.subheader("❌ Do powtórki")
    for s in sorted(st.session_state.niezaliczone):
        if s not in st.session_state.zaliczone: # Pokazuj tylko jeśli jeszcze nie poprawiono
            st.write(f"📌 {s}")

# --- GŁÓWNY PANEL ---
st.title("🗂️ Interaktywne Fiszki")

if st.session_state.aktualne_pytanie:
    q = st.session_state.aktualne_pytanie
    st.subheader(f"Jak przetłumaczysz słowo: **{q['slowo']}**?")
    
    # Formularz quizu
    with st.form(key='fiszka_form'):
        wybor = st.radio("Wybierz opcję:", q['opcje'], index=None)
        submit = st.form_submit_button("Sprawdź odpowiedź")

    if submit:
        if wybor == q['poprawna']:
            st.success(f"Brawo! '{q['slowo']}' oznacza '{q['poprawna']}'.")
            st.session_state.zaliczone.add(q['slowo'])
            # Jeśli było w niezaliczonych, a teraz zgadliśmy - usuwamy z błędów
            if q['slowo'] in st.session_state.niezaliczone:
                st.session_state.niezaliczone.remove(q['slowo'])
            
            st.button("Następne słowo ➡️", on_click=lambda: st.session_state.update({"aktualne_pytanie": losuj_slowo()}))
        else:
            st.error(f"Niestety! Poprawna odpowiedź to: {q['poprawna']}")
            st.session_state.niezaliczone.add(q['slowo'])
            st.button("Spróbuj inne ➡️", on_click=lambda: st.session_state.update({"aktualne_pytanie": losuj_slowo()}))

else:
    st.balloons()
    st.success("GRATULACJE! Wszystkie słówka z obraz.png zostały zaliczone! 🎉")
    if st.button("Zacznij od nowa"):
        st.session_state.zaliczone = set()
        st.session_state.niezaliczone = set()
        st.session_state.aktualne_pytanie = losuj_slowo()
        st.rerun()

# Stopka z instrukcją dla wersji "wszędzie"
st.info("💡 Aby używać tego na telefonie: Wrzuć ten kod na GitHub i połącz z Streamlit Cloud.")
