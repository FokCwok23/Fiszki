import streamlit as st
import random
import yaml
import os

# --- ŁADOWANIE DANYCH Z PLIKU ---
def load_data():
    if os.path.exists("slowka.yaml"):
        with open("slowka.yaml", "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    else:
        st.error("Błąd: Nie znaleziono pliku slowka.yaml!")
        return {}

DANE_SLOWKA = load_data()

st.set_page_config(page_title="Fiszki Master", layout="wide")

# --- LOGIKA SESJI ---
if 'zaliczone' not in st.session_state:
    st.session_state.zaliczone = set()
if 'niezaliczone' not in st.session_state:
    st.session_state.niezaliczone = set()
if 'aktualne_pytanie' not in st.session_state:
    st.session_state.aktualne_pytanie = None
if 'pokaz_zdanie' not in st.session_state:
    st.session_state.pokaz_zdanie = False

def losuj_slowo():
    st.session_state.pokaz_zdanie = False
    dostepne = [s for s in DANE_SLOWKA.keys() if s not in st.session_state.zaliczone]
    if not dostepne:
        return None
    
    slowo = random.choice(dostepne)
    poprawna = DANE_SLOWKA[slowo]["PL"]
    inne = [v["PL"] for k, v in DANE_SLOWKA.items() if v["PL"] != poprawna]
    opcje = random.sample(inne, min(len(inne), 3)) + [poprawna]
    random.shuffle(opcje)
    
    return {"slowo": slowo, "poprawna": poprawna, "opcje": opcje, "sentence": DANE_SLOWKA[slowo]["Sentence"]}

def resetuj_postep():
    st.session_state.zaliczone = set()
    st.session_state.niezaliczone = set()
    st.session_state.aktualne_pytanie = losuj_slowo()
    st.toast("Postęp został zresetowany! 🧹")

if st.session_state.aktualne_pytanie is None:
    st.session_state.aktualne_pytanie = losuj_slowo()

# --- PASEK BOCZNY ---
with st.sidebar:
    st.header("📊 Twój Postęp")
    c1, c2 = st.columns(2)
    c1.metric("Zaliczone", len(st.session_state.zaliczone))
    c2.metric("Błędy", len(st.session_state.niezaliczone))
    
    if DANE_SLOWKA:
        procent = len(st.session_state.zaliczone) / len(DANE_SLOWKA)
        st.progress(procent)
        st.caption(f"Ukończono {int(procent*100)}% bazy")

    tab1, tab2 = st.tabs(["✅ Zaliczone", "❌ Błędy"])
    with tab1:
        for s in sorted(st.session_state.zaliczone):
            st.write(f"✔️ {s}")
    with tab2:
        for s in sorted(st.session_state.niezaliczone):
            if s not in st.session_state.zaliczone:
                st.write(f"📌 {s}")

    st.write("---")
    if st.button("🗑️ Wyczyść postęp", type="primary", use_container_width=True):
        resetuj_postep()
        st.rerun()

# --- GŁÓWNY PANEL ---
st.title("🗂️ Fiszki Angielskiego (YAML Mode)")

if st.session_state.aktualne_pytanie:
    q = st.session_state.aktualne_pytanie
    
    st.subheader(f"Jak przetłumaczysz: **{q['slowo']}**?")
    
    with st.form(key='fiszka_form'):
        wybor = st.radio("Wybierz opcję:", q['opcje'], index=None)
        submit = st.form_submit_button("Sprawdź!")

    if submit or st.session_state.pokaz_zdanie:
        if wybor == q['poprawna']:
            st.session_state.pokaz_zdanie = True
            st.success(f"✅ Świetnie! **{q['slowo']}** = **{q['poprawna']}**")
            
            # Wyróżnianie słowa w zdaniu
            clean_sentence = q['sentence'].replace(q['slowo'], f"***{q['slowo']}***")
            st.markdown(f"> **Example:** {clean_sentence}")
            
            st.session_state.zaliczone.add(q['slowo'])
            if q['slowo'] in st.session_state.niezaliczone:
                st.session_state.niezaliczone.remove(q['slowo'])
            
            st.button("Następne ➡️", on_click=lambda: st.session_state.update({"aktualne_pytanie": losuj_slowo()}))
        
        elif wybor is None:
            st.warning("Wybierz odpowiedź!")
        else:
            st.error(f"❌ Błąd. **{q['slowo']}** oznacza **{q['poprawna']}**.")
            st.session_state.niezaliczone.add(q['slowo'])
            st.button("Spróbuj inne słowo ➡️", on_click=lambda: st.session_state.update({"aktualne_pytanie": losuj_slowo()}))
else:
    st.success("🎉 Wszystkie słówka z pliku YAML opanowane!")
    if st.button("Zacznij od nowa"):
        resetuj_postep()
        st.rerun()
