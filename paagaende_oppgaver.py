
import streamlit as st
import json
import os
import uuid

DATA_FILE = "oppgaver_data.json"

st.set_page_config(page_title="Pågående oppgaver", layout="centered")

# Hjelpefunksjon for å laste og lagre oppgaver
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"oppgaver": [], "fullfort": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Last inn eksisterende data
data = load_data()

# Initier session state
for key in ["new_title", "new_description", "new_wait", "new_comment"]:
    if key not in st.session_state:
        if key == "new_wait":
            st.session_state[key] = False
        else:
            st.session_state[key] = ""

st.title("✅ Pågående oppgaver")

# VIS PÅGÅENDE OPPGAVER ØVERST
st.subheader("Dine oppgaver:")

oppgaver_som_ikke_er_fullfort = [o for o in data["oppgaver"] if o.get("prosent", 0) < 100]

for o in oppgaver_som_ikke_er_fullfort:
    key = f"slider_{o['id']}"
    prosent = st.slider(
        f"{o['title']} – {o.get('description', '')}",
        min_value=0,
        max_value=100,
        value=o.get("prosent", 0),
        key=key,
        help="Dra for å oppdatere fremdrift"
    )
    if o.get("venter", False) and o.get("kommentar"):
        st.markdown(f"🕒 *Venter på:* {o['kommentar']}")
    o["prosent"] = prosent

    if prosent == 100:
        st.success("🎉 Oppgave fullført! Fantastisk innsats!")
        data["oppgaver"].remove(o)
        data["fullfort"].append(o)
        save_data(data)
        st.experimental_rerun()

save_data(data)

# SKJEMA FOR NY OPPGAVE UNDER
st.subheader("Legg til ny oppgave:")

st.text_input("Tittel", key="new_title")
st.text_area("Beskrivelse", key="new_description")
st.checkbox("Venter på noen?", key="new_wait")

if st.session_state["new_wait"]:
    st.text_input("Kommentar til hva du venter på", key="new_comment")

if st.button("Legg til oppgave"):
    ny_oppgave = {
        "id": str(uuid.uuid4()),
        "title": st.session_state.new_title,
        "description": st.session_state.new_description,
        "venter": st.session_state.new_wait,
        "kommentar": st.session_state.new_comment if st.session_state.new_wait else "",
        "prosent": 0
    }
    data["oppgaver"].append(ny_oppgave)
    save_data(data)

    # Nullstill feltene
    st.session_state.new_title = ""
    st.session_state.new_description = ""
    st.session_state.new_wait = False
    st.session_state.new_comment = ""

    st.experimental_rerun()
