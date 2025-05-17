
import streamlit as st
import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("data.json")

# Initialiser state
for key in ["new_title", "new_desc", "new_wait", "new_comment"]:
    if key not in st.session_state:
        st.session_state[key] = ""

if "oppgaver" not in st.session_state:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            st.session_state.oppgaver = json.load(f)
    else:
        st.session_state.oppgaver = []

if "ferdige" not in st.session_state:
    st.session_state.ferdige = []

if "prosent" not in st.session_state:
    st.session_state.prosent = {}

st.title("✅ Mine oppgaver")
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", len(st.session_state.oppgaver))
col2.metric("Ferdig", len(st.session_state.ferdige))
col3.metric("Snitt tid", "-")

st.subheader("➕ Legg til ny oppgave")
st.session_state["new_title"] = st.text_input("Tittel", key="new_title")
st.session_state["new_desc"] = st.text_area("Beskrivelse", key="new_desc")
st.session_state["new_wait"] = st.checkbox("Venter på noen?", key="new_wait")
if st.session_state["new_wait"]:
    st.session_state["new_comment"] = st.text_input("Hva venter du på?", key="new_comment")

if st.button("Legg til oppgave"):
    if st.session_state["new_title"]:
        ny = {
            "id": len(st.session_state.oppgaver),
            "tittel": st.session_state["new_title"],
            "beskrivelse": st.session_state["new_desc"],
            "venter": st.session_state["new_wait"],
            "kommentar": st.session_state["new_comment"] if st.session_state["new_wait"] else "",
            "startet": str(datetime.now()),
        }
        st.session_state.oppgaver.append(ny)
        with open(DATA_FILE, "w") as f:
            json.dump(st.session_state.oppgaver, f)
        st.success("✅ Ny oppgave registrert!")
    else:
        st.error("❌ Tittel kan ikke være tom.")

st.subheader("🔍 Pågående oppgaver")
for o in st.session_state.oppgaver:
    with st.expander(o["tittel"]):
        st.write(o["beskrivelse"])
        if o["venter"]:
            st.info(f"⚠️ Venter på: {o['kommentar']}")
        st.slider("Fremdrift (%)", 0, 100, key=f"slider_{o['id']}")
