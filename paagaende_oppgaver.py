
import streamlit as st
import json
import os
from datetime import datetime
import random

# Path to data file
DATA_PATH = "todo_data.json"

# Load or initialize data
def load_data():
    if not os.path.exists(DATA_PATH):
        # Return empty structure if file missing
        return {"oppgaver": [], "fullfort": []}
    with open(DATA_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    # Ensure keys exist
    data.setdefault("oppgaver", [])
    data.setdefault("fullfort", [])
    return data

# Save data back to file
def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

# Initialize Streamlit layout
st.set_page_config(page_title="Mine oppgaver", layout="centered")
st.title("✅ Mine oppgaver")

# Load data
data = load_data()

# KPI display
st.subheader("📊 Status")
totalt = len(data["oppgaver"]) + len(data["fullfort"])
ferdig = len(data["fullfort"])
if ferdig > 0:
    tider = [
        (datetime.fromisoformat(o["ferdig_tid"]) - datetime.fromisoformat(o["start_tid"])).total_seconds()
        for o in data["fullfort"] if "start_tid" in o and "ferdig_tid" in o
    ]
    snitt_tid = f"{round(sum(tider)/len(tider)/60,1)} min"
else:
    snitt_tid = "-"
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", totalt)
col2.metric("Ferdig", ferdig)
col3.metric("Snitt tid", snitt_tid)

st.markdown("---")

# Add new task form
with st.form("ny_oppgave", clear_on_submit=True):
    st.subheader("➕ Legg til ny oppgave")
    tittel = st.text_input("Tittel")
    beskrivelse = st.text_area("Beskrivelse")
    venter = st.checkbox("Venter på noen?")
    kommentar = ""
    if venter:
        kommentar = st.text_input("Hva venter du på?", placeholder="Beskriv hvem eller hva du venter på")
    submitted = st.form_submit_button("Legg til")
    if submitted:
        if len(data["oppgaver"]) >= 10:
            st.warning(random.choice([
                "🚫 Maks 10 oppgaver! Fullfør noen før du legger til nye.",
                "⚠️ Du har nådd grensen – rydd opp først!"
            ]))
        elif not tittel:
            st.error("Tittel kan ikke være tom.")
        else:
            # Append new task
            data["oppgaver"].append({
                "tittel": tittel,
                "beskrivelse": beskrivelse,
                "status": [False]*10,
                "start_tid": datetime.now().isoformat(),
                "venter": venter,
                "kommentar": kommentar
            })
            save_data(data)
            st.success(random.choice([
                "✅ Oppgave lagt til!",
                "📝 Ny oppgave registrert!"
            ]))
            st.experimental_rerun()

# Display active tasks
for idx, oppg in enumerate(data["oppgaver"]):
    with st.expander(oppg["tittel"]):
        st.write(oppg["beskrivelse"])
        if oppg.get("venter"):
            st.info(f"⚠️ Venter: {oppg.get('kommentar','')}")
        cols = st.columns(10)
        for i in range(10):
            if cols[i].checkbox("", value=oppg["status"][i], key=f"{idx}_{i}"):
                oppg["status"][i] = True
        prosent = sum(oppg["status"])*10
        st.progress(prosent, text=f"{prosent}% fullført")
        if prosent==100:
            # Mark completed
            oppg["ferdig_tid"] = datetime.now().isoformat()
            data["fullfort"].append(oppg)
            data["oppgaver"].pop(idx)
            save_data(data)
            st.success("🎉 Oppgave fullført!")
            st.experimental_rerun()
