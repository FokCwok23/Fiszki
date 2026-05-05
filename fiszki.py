import streamlit as st
import random

# Rozbudowana baza danych z obraz.png
DANE_SLOWKA = {
    "Exceptional": "wyjątkowy", "Stunning": "zachwycający", "Hideous": "paskudny",
    "Appalling": "przerażający/beznadziejny", "Vast": "ogromny", "Minute": "malutki",
    "Essential": "niezbędny", "Crucial": "kluczowy", "Tedious": "nużący",
    "Hilarious": "komiczny", "Thrilled": "podekscytowany", "Miserable": "nieszczęśliwy",
    "Vivid": "obrazowy/wyrazisty", "Straightforward": "jasny/prosty", "Obscure": "niejasny/mało znany",
    "Ambiguous": "dwuznaczny", "Sceptical": "sceptyczny", "Inevitable": "nieunikniony",
    "Remarkable": "godny uwagi", "Profound": "głęboki", "To enhance": "ulepszać/wzmacniać",
    "To diminish": "zmniejszać się", "To maintain": "utrzymywać", "To acquire": "nabywać",
    "To obtain": "uzyskiwać", "To clarify": "wyjaśniać", "To emphasize": "podkreślać",
    "Furthermore": "ponadto", "Moreover": "co więcej", "Nevertheless": "niemniej jednak",
    "Consequently": "w rezultacie", "Thus": "zatem", "Alternatively": "ewentualnie",
    "Significantly": "znacząco", "Undoubtedly": "niewątpliwie", "Advantage": "zaleta",
    "Drawback": "wada", "Benefit": "korzyść", "Solution": "rozwiązanie",
    "Obstacle": "przeszkoda", "Development": "rozwój", "Approach": "podejście",
    "Impact": "wpływ", "Tendency": "tendencja", "Diversity": "różnorodność"
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
    # Zabezpieczenie przed małą liczbą słówek w bazie
    opcje = random.sample(inne, min(len(inne), 3)) + [poprawna]
    random.shuffle(opcje)
    
    return {"slowo": slowo, "poprawna": poprawna, "opcje": opcje}

def resetuj_postep():
    st.session_state.zaliczone = set()
    st.session_state.niezaliczone = set()
    st.session_state.aktualne_pytanie = losuj_slowo()
    st.toast("Postęp został zresetowany! 🧹")

# Inicjalizacja pierwszego pytania
if st.session_state.aktualne_pytanie is None:
    st.session_state.aktualne_pytanie = losuj_slowo()

# --- PASEK BOCZNY (SIDEBAR) ---
with st.sidebar:
    st.header("📊 Twój Postęp")
    
    # Statystyki
    c1, c2 = st.columns(2)
    c1.metric("Zaliczone", len(st.session_state.zaliczone))
    c2.metric("Błędy", len(st.session_state.niezaliczone))
    
    # Pasek postępu
    procent = len(st.session_state.zaliczone) / len(DANE_SLOWKA)
    st.progress(procent)
    st.caption(f"Ukończono {int(procent*100)}% bazy słówek")

    st.write("---")
    
    # Listy słówek
    tab1, tab2 = st.tabs(["✅ Zaliczone", "❌ Błędy"])
    with tab1:
        for s in sorted(st.session_state.zaliczone):
            st.write(f"✔️ {s}")
    with tab2:
        for s in sorted(st.session_state.niezaliczone):
            if s not in st.session_state.zaliczone:
                st.write(f"📌 {s}")

    st.write("---")
    # PRZYCISK RESETU
    if st.button("🗑️ Wyczyść postęp", type="primary", use_container_width=True):
        resetuj_postep()
        st.rerun()

# --- GŁÓWNY PANEL ---
st.title("🗂️ Fiszki Angielskiego")

if st.session_state.aktualne_pytanie:
    q = st.session_state.aktualne_pytanie
    
    st.info(f"Pytanie dla Ciebie:")
    st.subheader(f"Jak przetłumaczysz: **{q['slowo']}**?")
    
    with st.form(key='fiszka_form', clear_on_submit=True):
        wybor = st.radio("Wybierz jedną z opcji:", q['opcje'], index=None)
        submit = st.form_submit_button("Sprawdź!")

    if submit:
        if wybor == q['poprawna']:
            st.success(f"Świetnie! **{q['slowo']}** to rzeczywiście **{q['poprawna']}**.")
            st.session_state.zaliczone.add(q['slowo'])
            if q['slowo'] in st.session_state.niezaliczone:
                st.session_state.niezaliczone.remove(q['slowo'])
            st.button("Następne ➡️", on_click=lambda: st.session_state.update({"aktualne_pytanie": losuj_slowo()}))
        elif wybor is None:
            st.warning("Wybierz odpowiedź przed sprawdzeniem!")
        else:
            st.error(f"Nie tym razem. **{q['slowo']}** oznacza **{q['poprawna']}**.")
            st.session_state.niezaliczone.add(q['slowo'])
            st.button("Spróbuj inne słowo ➡️", on_click=lambda: st.session_state.update({"aktualne_pytanie": losuj_slowo()}))

else:
    st.balloons()
    st.success("🎉 Woow! Wszystkie słówka z listy opanowane!")
    if st.button("Zacznij od nowa (Reset)", type="primary"):
        resetuj_postep()
        st.rerun()
