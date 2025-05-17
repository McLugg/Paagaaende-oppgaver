
import streamlit as st
import json
import os
import uuid

DATA_FILE = "data.json"
GREEN = "#5FAA58"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"oppgaver": [], "fullfort": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

st.title("Pågående oppgaver")

# Vise pågående oppgaver først
st.header("Pågående oppgaver")
for o in data["oppgaver"]:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"**{o['title']}**")
        if o.get("venter", False):
            st.markdown(f"_Venter på_: {o.get('kommentar', '')}")
    with col2:
        key = f"slider_{o['id']}"
        prosent = st.slider(
            "Fullført",
            0,
            100,
            int(o.get("prosent", 0)),
            key=key,
            label_visibility="collapsed"
        )
        o["prosent"] = prosent
        if prosent == 100 and o not in data["fullfort"]:
            data["oppgaver"].remove(o)
            data["fullfort"].append(o)
            st.success("🎉 Oppgaven er fullført! Bra jobba!")
            save_data(data)
            st.experimental_rerun()
save_data(data)

# Ny oppgave-seksjon nederst
st.header("Legg til ny oppgave")

if "new_title" not in st.session_state:
    st.session_state["new_title"] = ""
if "new_wait" not in st.session_state:
    st.session_state["new_wait"] = False
if "new_comment" not in st.session_state:
    st.session_state["new_comment"] = ""

st.text_input("Tittel", key="new_title")
venter = st.checkbox("Venter på noen?", key="new_wait")
if venter:
    st.text_input("Kommentar", key="new_comment")

if st.button("Legg til oppgave"):
    ny_oppgave = {
        "id": str(uuid.uuid4()),
        "title": st.session_state["new_title"],
        "venter": venter,
        "kommentar": st.session_state["new_comment"] if venter else "",
        "prosent": 0
    }
    data["oppgaver"].append(ny_oppgave)
    save_data(data)
    st.session_state["new_title"] = ""
    st.session_state["new_wait"] = False
    st.session_state["new_comment"] = ""
    st.experimental_rerun()
