
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

st.set_page_config(page_title="Mine oppgaver", layout="centered")
st.title("✅ Mine oppgaver")

data = load_data()
oppgaver = data["oppgaver"]
fullfort = data["fullfort"]

# KPI‐seksjon
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

# Ny oppgave
with st.form("ny_oppgave", clear_on_submit=True):
    st.subheader("➕ Legg til ny oppgave")
    tittel = st.text_input("Tittel")
    beskrivelse = st.text_area("Beskrivelse")
    venter = st.checkbox("Venter på noen?")
    kommentar = ""
    if venter:
        kommentar = st.text_input("Hva venter du på?", placeholder="Beskriv hvem eller hva du venter på")
    sendt = st.form_submit_button("Legg til")

    if sendt:
        if not tittel:
            st.error("❌ Tittel kan ikke være tom.")
        elif len(oppgaver) >= 10:
            st.warning("🚫 Maks 10 oppgaver! Fullfør noen før du legger til nye.")
        else:
            ny = {
                "tittel": tittel,
                "beskrivelse": beskrivelse,
                "status": [False]*10,
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
            st.experimental_rerun()

# Vis aktive oppgaver
for i, o in enumerate(list(oppgaver)):
    with st.expander(o["tittel"]):
        st.write(o["beskrivelse"])
        if o.get("venter"):
            st.info(f"⚠️ Venter på: {o.get('kommentar', '')}")
        cols = st.columns(10)
        for idx in range(10):
            checked = cols[idx].checkbox("", value=o["status"][idx], key=f"{i}-{idx}")
            o["status"][idx] = checked
        progresjon = sum(o["status"])*10
        st.progress(progresjon, text=f"{progresjon}%")
        if progresjon == 100:
            o["ferdig_tid"] = datetime.now().isoformat()
            fullfort.append(o)
            oppgaver.remove(o)
            save_data(data)
            st.success("🎉 Oppgave fullført!")
            st.experimental_rerun()
