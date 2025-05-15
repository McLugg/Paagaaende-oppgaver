
import streamlit as st
import json
import os
from datetime import datetime
import random

DATAFIL = "oppgaver_data.json"

# Hjelpefunksjon for å laste og lagre data
def last_data():
    if not os.path.exists(DATAFIL):
        return {"oppgaver": [], "fullfort": []}
    with open(DATAFIL, "r") as f:
        return json.load(f)

def lagre_data(data):
    with open(DATAFIL, "w") as f:
        json.dump(data, f)

# Sideoppsett
st.set_page_config(page_title="Mine oppgaver", layout="centered")

st.markdown("## ✅ Mine oppgaver")
st.markdown("### 📊 Status")

data = last_data()

# KPI
totalt = len(data["oppgaver"]) + len(data["fullfort"])
ferdig = len(data["fullfort"])
snitt_tid = "-"
tider = [oppg["tid"] for oppg in data["fullfort"] if "tid" in oppg]
if tider:
    snitt_tid = f"{sum(tider) / len(tider):.1f} sek"

col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", totalt)
col2.metric("Ferdig", ferdig)
col3.metric("Snitt tid", snitt_tid)

st.markdown("---")
st.markdown("### ➕ Legg til ny oppgave")

# Interaktiv oppgaveoppretting
ny_tittel = st.text_input("Tittel", key="ny_tittel")
ny_beskrivelse = st.text_area("Beskrivelse", key="ny_beskrivelse")

venter = st.checkbox("Venter på noen?", key="venter_valg")

venter_kommentar = ""
if venter:
    venter_kommentar = st.text_input("Hva venter du på?", key="venter_kommentar")

if st.button("Legg til"):
    if len(data["oppgaver"]) >= 10:
        st.warning("🚫 Du kan maks ha 10 oppgaver. Fullfør noen før du legger til flere.")
    elif ny_tittel.strip() == "":
        st.warning("Tittel kan ikke være tom.")
    else:
        ny_oppgave = {
            "tittel": ny_tittel,
            "beskrivelse": ny_beskrivelse,
            "status": [0]*10,
            "startet": datetime.now().timestamp(),
            "venter": venter,
            "kommentar": venter_kommentar if venter else ""
        }
        data["oppgaver"].append(ny_oppgave)
        lagre_data(data)
        st.success("✅ Oppgave lagt til!")

