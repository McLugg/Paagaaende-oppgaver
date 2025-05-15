
import streamlit as st
import json
import os
import time
from datetime import datetime
from uuid import uuid4

st.set_page_config(page_title="Mine oppgaver", layout="centered")

DATAFIL = "data.json"

if "venter" not in st.session_state:
    st.session_state.venter = False

if "venter_kommentar" not in st.session_state:
    st.session_state.venter_kommentar = ""

def last_data():
    if os.path.exists(DATAFIL):
        with open(DATAFIL, "r") as f:
            return json.load(f)
    else:
        return {"oppgaver": [], "fullfort": []}

def lagre_data(data):
    with open(DATAFIL, "w") as f:
        json.dump(data, f)

data = last_data()

st.title("✅ Mine oppgaver")

# Statistikk
st.subheader("📊 Status")
totalt = len(data["oppgaver"]) + len(data["fullfort"])
ferdig = len(data["fullfort"])
snitt_tid = "-"
if ferdig > 0:
    tider = [o["ferdig_tid"] - o["start_tid"] for o in data["fullfort"]]
    snitt_tid = round(sum(tider) / ferdig / 60, 1)

col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", totalt)
col2.metric("Ferdig", ferdig)
col3.metric("Snitt tid", snitt_tid if snitt_tid != "-" else "-")

# Ny oppgave
st.subheader("➕ Legg til ny oppgave")

with st.form("ny_oppgave_form", clear_on_submit=True):
    tittel = st.text_input("Tittel")
    beskrivelse = st.text_area("Beskrivelse")
    venter = st.checkbox("Venter på noen?", value=st.session_state.venter)
    if venter:
        kommentar = st.text_input("Hva venter du på?")
    else:
        kommentar = ""
    sendt = st.form_submit_button("Legg til")

    if sendt:
        if len(data["oppgaver"]) >= 10:
            st.warning("Du har nådd maks 10 oppgaver. Fullfør noen før du legger til flere.")
        else:
            ny = {
                "id": str(uuid4()),
                "tittel": tittel,
                "beskrivelse": beskrivelse,
                "status": [False]*10,
                "venter": venter,
                "kommentar": kommentar,
                "start_tid": time.time()
            }
            data["oppgaver"].append(ny)
            lagre_data(data)
            st.success("✅ Oppgave lagt til!")

# Vis oppgaver
for oppgave in data["oppgaver"]:
    st.markdown("---")
    st.markdown(f"**{oppgave['tittel']}**")
    st.markdown(oppgave["beskrivelse"])

    if oppgave["venter"]:
        st.info(f"⚠️ Venter: {oppgave.get('kommentar', '')}")

    # Fremgang
    cols = st.columns(10)
    for i in range(10):
        with cols[i]:
            if st.checkbox(" ", value=oppgave["status"][i], key=f"{oppgave['id']}_{i}"):
                oppgave["status"][i] = True

    # Progress bar
    prosent = sum(oppgave["status"]) * 10
    st.progress(prosent, text=f"{prosent}% fullført")

    # Hvis alle fullført
    if all(oppgave["status"]):
        st.success(f"🎉 Oppgave fullført: {oppgave['tittel']}")
        oppgave["ferdig_tid"] = time.time()
        data["fullfort"].append(oppgave)
        data["oppgaver"] = [o for o in data["oppgaver"] if o["id"] != oppgave["id"]]
        lagre_data(data)
        st.rerun()
