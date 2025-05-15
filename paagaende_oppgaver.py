
import streamlit as st
import json
import os
from datetime import datetime
import random

DATA_PATH = "data.json"

st.set_page_config(page_title="Mine oppgaver", layout="centered")

st.markdown("# ✅ Mine oppgaver")

def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    else:
        return {"oppgaver": [], "fullfort": []}

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

# KPIs
st.markdown("### 📊 Status")
total = len(data["oppgaver"]) + len(data["fullfort"])
ferdig = len(data["fullfort"])
if ferdig > 0:
    snitt_tid = sum([(datetime.now() - datetime.strptime(o["opprettet"], "%Y-%m-%d %H:%M:%S")).total_seconds() for o in data["fullfort"]]) / ferdig
    snitt_tid = f"{round(snitt_tid / 60, 1)} min"
else:
    snitt_tid = "-"
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", total)
col2.metric("Ferdig", ferdig)
col3.metric("Snitt tid", snitt_tid)

# Legg til ny oppgave
st.markdown("---")
st.markdown("### ➕ Legg til ny oppgave")
with st.form("legg_til_oppgave"):
    tittel = st.text_input("Tittel")
    beskrivelse = st.text_area("Beskrivelse")
    venter = st.checkbox("Venter på noen?")
    venter_paa = ""
    if venter:
        venter_paa = st.text_input("Hva venter du på?", placeholder="Skriv hvem eller hva du venter på")
    submitted = st.form_submit_button("Legg til")
    if submitted:
        if len(data["oppgaver"]) >= 10:
            st.warning(random.choice([
                "🚫 Oi! Du har allerede 10 oppgaver. Fullfør noen først!",
                "📋 Maksgrensen er nådd – rydd litt i listen 🧹",
                "😅 Du multitasker hardt – prøv å gjøre ferdig én først!"
            ]))
        else:
            data["oppgaver"].append({
                "tittel": tittel,
                "beskrivelse": beskrivelse,
                "status": [0]*10,
                "opprettet": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "venter": venter,
                "venter_paa": venter_paa
            })
            save_data(data)
            st.success(random.choice([
                "✅ Nice! En ny oppgave er lagt til!",
                "🚀 Bra jobba! Du er i flytsonen!",
                "📝 Ny oppgave lagt til. Du fikser dette!"
            ]))
            st.experimental_rerun()
