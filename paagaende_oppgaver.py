
import streamlit as st
import json
import uuid
import os
import time
from datetime import datetime
from PIL import Image

DATA_FILE = "data.json"

st.set_page_config(layout="wide")

st.markdown("<h1 style='font-size: 36px;'>✅ Mine oppgaver</h1>", unsafe_allow_html=True)

# Initialiser data
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"oppgaver": []}, f)

def last_oppgaver():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def lagre_oppgaver(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = last_oppgaver()

# Statistikk
fullforte = [o for o in data["oppgaver"] if o.get("ferdig")]
ferdige_tider = [o["fullfort_tidspunkt"] - o["start_tidspunkt"] for o in fullforte if o.get("fullfort_tidspunkt") and o.get("start_tidspunkt")]
snitt_tid = sum(ferdige_tider)/len(ferdige_tider)/60 if ferdige_tider else None

col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", len(data["oppgaver"]))
col2.metric("Ferdig", len(fullforte))
col3.metric("Snitt tid", f"{snitt_tid:.1f} min" if snitt_tid else "-")

# Pågående oppgaver først
st.markdown("### 🔍 Pågående oppgaver")
for o in data["oppgaver"]:
    if o.get("ferdig"):
        continue

    with st.expander(f"{o['tittel']}"):
        st.write(o["beskrivelse"])
        if o.get("venter_pa"):
            st.info(f"⚠️ Venter på: {o['venter_pa']}")

        prosent = st.slider("Fremdrift (%)", 0, 100, o.get("fremdrift", 0), key=f"slider_{o['id']}")
        o["fremdrift"] = prosent

        st.progress(prosent / 100)

        if prosent == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
            o["ferdig"] = True
            o["fullfort_tidspunkt"] = time.time()

lagre_oppgaver(data)

# Legg til ny oppgave
st.markdown("### ➕ Legg til ny oppgave")
with st.form("legg_til_oppgave"):
    ny_tittel = st.text_input("Oppgavetittel", key="new_title")
    ny_beskrivelse = st.text_area("Beskrivelse", key="new_desc")
    ny_venter = st.checkbox("Venter på noen?", key="new_wait")
    ny_kommentar = ""
    if ny_venter:
        ny_kommentar = st.text_input("Hva venter du på?", key="new_comment")

    if st.form_submit_button("Legg til oppgave"):
        if not ny_tittel.strip():
            st.error("❌ Tittel kan ikke være tom.")
        else:
            ny_oppgave = {
                "id": str(uuid.uuid4()),
                "tittel": ny_tittel,
                "beskrivelse": ny_beskrivelse,
                "fremdrift": 0,
                "ferdig": False,
                "start_tidspunkt": time.time(),
            }
            if ny_venter:
                ny_oppgave["venter_pa"] = ny_kommentar
            data["oppgaver"].append(ny_oppgave)
            lagre_oppgaver(data)
            st.success("🚀 Ny oppgave registrert!")
