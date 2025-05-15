
import streamlit as st
import json
import os
from datetime import datetime
import random

st.set_page_config(page_title="Mine oppgaver", page_icon="✅")

DATAFIL = "data.json"

# Initialiser datafil
if not os.path.exists(DATAFIL):
    with open(DATAFIL, "w") as f:
        json.dump({"oppgaver": [], "fullfort": []}, f)

# Last inn data
with open(DATAFIL, "r") as f:
    data = json.load(f)

st.title("✅ Mine oppgaver")

# KPI-visning
st.subheader("📊 Status")
totalt = len(data["oppgaver"]) + len(data["fullfort"])
ferdig = len(data["fullfort"])
snitt_tid = "-"
if ferdig > 0:
    tider = [(datetime.strptime(o["ferdig"], "%Y-%m-%d %H:%M:%S") - datetime.strptime(o["startet"], "%Y-%m-%d %H:%M:%S")).total_seconds() for o in data["fullfort"]]
    snitt_tid = f"{int(sum(tider)/len(tider)//60)} min"

col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", totalt)
col2.metric("Ferdig", ferdig)
col3.metric("Snitt tid", snitt_tid)

st.markdown("---")

# Legg til ny oppgave
with st.form("legg_til"):
    st.subheader("➕ Legg til ny oppgave")
    tittel = st.text_input("Tittel")
    beskrivelse = st.text_area("Beskrivelse")
    venter = st.checkbox("Venter på noen?")
    kommentar = ""
    if venter:
        kommentar = st.text_input("Hva venter du på?", key="kommentarfelt")
    sendt = st.form_submit_button("Legg til")
    if sendt and len(data["oppgaver"]) >= 10:
        st.warning(random.choice([
            "🚧 Fullt! Løs noe først 😅",
            "😬 10 oppgaver er maks – ta tak i en!",
            "🤖 Prioritering før produktivitet – rydd litt!"
        ]))
    elif sendt and tittel:
        data["oppgaver"].append({
            "tittel": tittel,
            "beskrivelse": beskrivelse,
            "status": [False]*10,
            "startet": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "venter": venter,
            "kommentar": kommentar
        })
        with open(DATAFIL, "w") as f:
            json.dump(data, f)
        st.success(random.choice([
            "✅ Bra jobba! En ny utfordring er lagt til!",
            "🎯 Klar for innsats! Oppgaven er registrert.",
            "📌 Ny oppgave lagt til – du fikser dette!"
        ]))
        st.experimental_rerun()

# Vis oppgaver
for i, oppgave in enumerate(data["oppgaver"]):
    med = st.container()
    med.subheader(oppgave["tittel"])
    med.write(oppgave["beskrivelse"])

    cols = med.columns(10)
    for j in range(10):
        if cols[j].checkbox("", value=oppgave["status"][j], key=f"{i}_{j}"):
            oppgave["status"][j] = True

    prosent = sum(oppgave["status"]) * 10
    med.progress(prosent, f"{prosent}% fullført")

    if oppgave.get("venter") and oppgave.get("kommentar"):
        med.info(f"⚠️ Venter: {oppgave['kommentar']}")

    if all(oppgave["status"]):
        st.toast(random.choice([
            "🎉 Fullført! Du ruler!",
            "🚀 Ferdig – på tide med en pause?",
            "👏 Oppdrag utført, sjefen!"
        ]), icon="🎉")
        oppgave["ferdig"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["fullfort"].append(oppgave)
        data["oppgaver"].pop(i)
        with open(DATAFIL, "w") as f:
            json.dump(data, f)
        st.experimental_rerun()
