import streamlit as st
import random

# Rozszerzona baza o przykładowe zdania dla każdego słowa z obraz.png
DANE_SLOWKA = {
    "Exceptional": {"PL": "wyjątkowy", "Sentence": "The service at this hotel was truly exceptional."},
    "Stunning": {"PL": "zachwycający", "Sentence": "The view from the top of the mountain is stunning."},
    "Hideous": {"PL": "paskudny", "Sentence": "I think that bright neon wallpaper is absolutely hideous."},
    "Appalling": {"PL": "przerażający/beznadziejny", "Sentence": "The conditions in the prison were appalling."},
    "Vast": {"PL": "ogromny", "Sentence": "The Sahara Desert is a vast area of sand and rock."},
    "Minute": {"PL": "malutki", "Sentence": "You need to be careful; there are minute traces of dust on the lens."},
    "Essential": {"PL": "niezbędny", "Sentence": "Water is essential for all living things."},
    "Crucial": {"PL": "kluczowy", "Sentence": "It is crucial that we reach a decision today."},
    "Tedious": {"PL": "nużący", "Sentence": "The job was tedious and repetitive, but it paid well."},
    "Hilarious": {"PL": "komiczny", "Sentence": "He told us a hilarious story about his trip to France."},
    "Thrilled": {"PL": "podekscytowany", "Sentence": "She was thrilled to hear that she got the job."},
    "Miserable": {"PL": "nieszczęśliwy", "Sentence": "The cold, rainy weather made everyone feel miserable."},
    "Vivid": {"PL": "obrazowy/wyrazisty", "Sentence": "I have a very vivid memory of my first day at school."},
    "Straightforward": {"PL": "jasny/prosty", "Sentence": "The instructions were very straightforward and easy to follow."},
    "Obscure": {"PL": "niejasny/mało znany", "Sentence": "He is a fan of obscure 1970s jazz bands."},
    "Ambiguous": {"PL": "dwuznaczny", "Sentence": "His reply to my question was somewhat ambiguous."},
    "Sceptical": {"PL": "sceptyczny", "Sentence": "I am sceptical about the chances of the project succeeding."},
    "Inevitable": {"PL": "nieunikniony", "Sentence": "The accident was the inevitable result of carelessness."},
    "Remarkable": {"PL": "godny uwagi", "Sentence": "It is remarkable that she survived the crash."},
    "Profound": {"PL": "głęboki", "Sentence": "The invention of the internet had a profound effect on society."},
    "To enhance": {"PL": "ulepszać/wzmacniać", "Sentence": "Good lighting will enhance the beauty of the room."},
    "To diminish": {"PL": "zmniejszać się", "Sentence": "The pain will gradually diminish over time."},
    "To maintain": {"PL": "utrzymywać", "Sentence": "You must maintain a steady speed on the highway."},
    "To acquire": {"PL": "nabywać", "Sentence": "I managed to acquire a rare first edition of the book."},
    "To obtain": {"PL": "uzyskiwać", "Sentence": "Further information can be obtained from our office."},
    "To clarify": {"PL": "wyjaśniać", "Sentence": "Could you clarify what you mean by 'provisional'?"},
    "Furthermore": {"PL": "ponadto", "Sentence": "The house is beautiful; furthermore, it's in a great location."},
    "Consequently": {"PL": "w rezultacie", "Sentence": "He didn't study; consequently, he failed the exam."},
    "Cope with": {"PL": "radzić sobie z", "Sentence": "It's difficult to cope with so much stress at once."},
    "Come up with": {"PL": "wymyślić", "Sentence": "We need to come up with a new plan immediately."},
    "A double-edged sword": {"PL": "miecz obosieczny", "Sentence": "Fame can be a double-edged sword."},
    "The tip of the iceberg": {"PL": "wierzchołek góry lodowej", "Sentence": "These complaints are just the tip of the iceberg."},
    "Under the weather": {"PL": "czuć się niewyraźnie", "Sentence": "I'm feeling a bit under the weather today."}
}

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

    if st.button("🗑️ Wyczyść postęp", type="primary", use_container_width=True):
        resetuj_postep()
        st.rerun()

# --- GŁÓWNY PANEL ---
st.title("🗂️ Fiszki Angielskiego")

if st.session_state.aktualne_pytanie:
    q = st.session_state.aktualne_pytanie
    
    st.subheader(f"Jak przetłumaczysz: **{q['slowo']}**?")
    
    # Używamy kontenera, aby móc czyścić radio po przejściu dalej
    with st.form(key='fiszka_form'):
        wybor = st.radio("Wybierz opcję:", q['opcje'], index=None)
        submit = st.form_submit_button("Sprawdź!")

    if submit or st.session_state.pokaz_zdanie:
        if wybor == q['poprawna']:
            st.session_state.pokaz_zdanie = True
            st.success(f"✅ Świetnie! **{q['slowo']}** = **{q['poprawna']}**")
            
            # POKAZYWANIE ZDANIA
            st.markdown(f"""
            > **Example sentence:**  
            > {q['sentence'].replace(q['slowo'], f"**{q['slowo']}**").replace(q['slowo'].lower(), f"**{q['slowo'].lower()}**")}
            """)
            
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
    st.balloons()
    st.success("🎉 Wszystkie słówka opanowane!")
    if st.button("Zacznij od nowa", type="primary"):
        resetuj_postep()
        st.rerun()
