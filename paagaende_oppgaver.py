
import streamlit as st
import json
import os
from datetime import datetime
import random

# File where tasks are stored
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

# KPI section
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
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", totalt)
col2.metric("Ferdig", ferdig)
col3.metric("Snitt tid", snitt)

st.markdown("---")

# New task input (dynamic comment field)
st.subheader("➕ Legg til ny oppgave")
tittel = st.text_input("Tittel")
beskrivelse = st.text_area("Beskrivelse")
venter = st.checkbox("Venter på noen?")
venter_kommentar = ""
if venter:
    venter_kommentar = st.text_input("Hva venter du på?", placeholder="Beskriv hvem eller hva du venter på")

if st.button("Legg til oppgave"):
    if not tittel.strip():
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
            "kommentar": venter_kommentar
        }
        oppgaver.append(ny)
        save_data(data)
        st.success(random.choice([
            "✅ Oppgave lagt til!",
            "📝 Klar for innsats!",
            "🚀 Ny oppgave registrert!"
        ]))

st.markdown("---")
st.subheader("🔍 Pågående oppgaver")
for idx, o in enumerate(list(oppgaver)):
    with st.expander(o["tittel"]):
        st.write(o["beskrivelse"])
        if o.get("venter"):
            st.info(f"⚠️ Venter på: {o.get('kommentar','')}")
        cols = st.columns(10)
        for i in range(10):
            checked = cols[i].checkbox("", value=o["status"][i], key=f"{idx}_{i}")
            o["status"][i] = checked
        progresjon = sum(o["status"]) * 10
        st.progress(progresjon/100, text=f"{progresjon}%")
        if progresjon == 100:
            o["ferdig_tid"] = datetime.now().isoformat()
            fullfort.append(o)
            oppgaver.remove(o)
            save_data(data)
            st.success("🎉 Oppgave fullført!")
