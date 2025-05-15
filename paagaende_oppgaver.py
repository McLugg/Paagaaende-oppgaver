
import streamlit as st
import json
import os
from datetime import datetime
import random

# Path to data file
DATA_PATH = "data.json"

def load_data():
    if not os.path.exists(DATA_PATH):
        return {"oppgaver": [], "fullfort": []}
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}
    data.setdefault("oppgaver", [])
    data.setdefault("fullfort", [])
    return data

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

# Initialize session state for form inputs
for key, default in [("tittel", ""), ("beskrivelse", ""), ("venter", False), ("kommentar", "")]:
    if key not in st.session_state:
        st.session_state[key] = default

# App UI
st.set_page_config(page_title="Mine oppgaver", layout="centered")
st.title("✅ Mine oppgaver")

data = load_data()
oppgaver = data["oppgaver"]
fullfort = data["fullfort"]

# KPI Section
st.subheader("📊 Status")
totalt = len(oppgaver) + len(fullfort)
ferdig = len(fullfort)
if ferdig > 0:
    tider = []
    for o in fullfort:
        if "start_tid" in o and "ferdig_tid" in o:
            start = datetime.fromisoformat(o["start_tid"])
            ferdig_tid = datetime.fromisoformat(o["ferdig_tid"])
            tider.append((ferdig_tid - start).total_seconds())
    snitt = f"{round(sum(tider)/len(tider)/60,1)} min" if tider else "-"
else:
    snitt = "-"
c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", totalt)
c2.metric("Ferdig", ferdig)
c3.metric("Snitt tid", snitt)

st.markdown("---")

# New Task Form
st.subheader("➕ Legg til ny oppgave")
tittel = st.text_input("Tittel", key="tittel")
beskrivelse = st.text_area("Beskrivelse", key="beskrivelse")
venter = st.checkbox("Venter på noen?", key="venter")
kommentar = ""
if venter:
    kommentar = st.text_input("Hva venter du på?", key="kommentar", placeholder="Beskriv hvem eller hva du venter på")

if st.button("Legg til oppgave"):
    if not tittel.strip():
        st.error("❌ Tittel kan ikke være tom.")
    elif len(oppgaver) >= 10:
        st.warning("🚫 Maks 10 oppgaver! Fullfør noen før du legger til nye.")
    else:
        ny = {
            "tittel": tittel,
            "beskrivelse": beskrivelse,
            "status": 0,  # slider percentage
            "start_tid": datetime.now().isoformat(),
            "venter": venter,
            "kommentar": kommentar
        }
        oppgaver.append(ny)
        save_data(data)
        st.success(random.choice([
            "✅ Oppgave lagt til!",
            "📝 Klar for innsats!",
            "🚀 Ny oppgave registrert!"
        ]))
        # Reset form
        st.session_state.tittel = ""
        st.session_state.beskrivelse = ""
        st.session_state.venter = False
        st.session_state.kommentar = ""

st.markdown("---")
st.subheader("🔍 Pågående oppgaver")
for idx, o in enumerate(list(oppgaver)):
    with st.expander(o["tittel"]):
        st.write(o["beskrivelse"])
        if o.get("venter"):
            st.info(f"⚠️ Venter på: {o.get('kommentar','')}")
        # Slider for progress
        prosent = st.slider(
            "Fremgang (%)",
            min_value=0,
            max_value=100,
            step=10,
            value=o.get("status", 0),
            key=f"slider_{idx}"
        )
        o["status"] = prosent
        # Custom progress bar with green color
        bar_html = f'''
        <div style="background:#e0e0e0;border-radius:8px;overflow:hidden;">
          <div style="width:{prosent}%;background:#5FAA58;padding:4px 0;text-align:center;color:white;font-weight:bold;">
            {prosent}%
          </div>
        </div>
        '''
        st.markdown(bar_html, unsafe_allow_html=True)
        # Completion
        if prosent == 100:
            o["ferdig_tid"] = datetime.now().isoformat()
            fullfort.append(o)
            oppgaver.remove(o)
            save_data(data)
            st.balloons()
            st.success(random.choice([
                "🎉 Fantastisk jobba! Oppgaven er i boks!",
                "👏 Bra jobbet! Du fullførte en oppgave!",
                "🏆 Oppgave fullført – gå videre til neste!"
            ]))
