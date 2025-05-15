
import streamlit as st
import json
import time
from datetime import datetime
from pathlib import Path

DATAFIL = Path("data.json")

# Last eller initialiser data
if DATAFIL.exists():
    with open(DATAFIL, "r") as f:
        data = json.load(f)
else:
    data = {"oppgaver": [], "fullfort": []}

st.set_page_config(page_title="Mine oppgaver", page_icon="✅")

st.markdown("# ✅ Mine oppgaver")
st.markdown("### 📊 Status")

# KPI
totalt = len(data.get("oppgaver", [])) + len(data.get("fullfort", []))
ferdig = len(data.get("fullfort", []))
snitt_tid = "-"
if ferdig > 0:
    tider = [
        datetime.fromisoformat(o["ferdig"]) - datetime.fromisoformat(o["startet"])
        for o in data["fullfort"]
        if o.get("ferdig") and o.get("startet")
    ]
    snitt_tid = str(sum((t.total_seconds() for t in tider), 0) / ferdig / 60)[:4] + " min"

col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", totalt)
col2.metric("Ferdig", ferdig)
col3.metric("Snitt tid", snitt_tid)

st.divider()

# Legg til ny oppgave
st.markdown("### ➕ Legg til ny oppgave")
with st.form("ny_oppgave"):
    tittel = st.text_input("Tittel")
    beskrivelse = st.text_area("Beskrivelse", height=100)
    venter = st.checkbox("Venter på noen?")
    venter_paa = ""
    if venter:
        venter_paa = st.text_input("Hva venter du på?", placeholder="Skriv hvem eller hva du venter på")
    submit = st.form_submit_button("Legg til")

    if submit:
        if len(data["oppgaver"]) >= 10:
            st.warning("🚫 Du har allerede 10 oppgaver. Fullfør noen før du legger til flere.")
        elif not tittel:
            st.warning("⚠️ Oppgaven må ha en tittel.")
        else:
            oppgave = {
                "tittel": tittel,
                "beskrivelse": beskrivelse,
                "status": [0] * 10,
                "startet": datetime.now().isoformat(),
                "venter": venter,
                "venter_paa": venter_paa
            }
            data["oppgaver"].append(oppgave)
            with open(DATAFIL, "w") as f:
                json.dump(data, f, indent=2)
            st.success("✅ Oppgave lagt til!")

# TODO: Visning av oppgaver, fremdrift osv. kommer under her i neste steg
