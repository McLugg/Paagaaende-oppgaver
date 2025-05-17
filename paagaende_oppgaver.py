
import streamlit as st
import json
import uuid
from datetime import datetime

DATA_FILE = "data.json"

# Last inn data
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"oppgaver": [], "fullfort": []}

# Lagre data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

st.title("🧠 Pågående oppgaver")

# --- VIS PÅGÅENDE OPPGAVER FØRST ---
st.header("🚧 Pågående oppgaver")

for o in data["oppgaver"]:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"**{o['tittel']}**")
        if o.get("venter_pa"):
            st.write(f"⏳ Venter på: {o['venter_pa']}")
        key = f"slider_{o['id']}"
        prosent = st.slider("Fullført:", 0, 100, o["prosent"], key=key)
        if prosent != o["prosent"]:
            o["prosent"] = prosent
            if prosent == 100:
                data["oppgaver"].remove(o)
                o["ferdig_tid"] = datetime.now().isoformat()
                data["fullfort"].append(o)
                save_data(data)
                st.success("🚀 Oppgave fullført! Du er en maskin!")
                st.experimental_rerun()
            else:
                save_data(data)
    with col2:
        if st.button("🗑️", key=f"slett_{o['id']}"):
            data["oppgaver"].remove(o)
            save_data(data)
            st.experimental_rerun()

# --- SKJEMA FOR Å LEGGE TIL OPPGAVER ---
st.header("➕ Legg til ny oppgave")

if "new_wait" not in st.session_state:
    st.session_state["new_wait"] = False

new_title = st.text_input("Tittel", key="new_title")
st.session_state["new_wait"] = st.checkbox("Venter på noen?", value=st.session_state["new_wait"], key="wait_toggle")

venter_pa = ""
if st.session_state["new_wait"]:
    venter_pa = st.text_input("Hva venter du på?", key="venter_pa_input")

if st.button("Legg til oppgave"):
    if new_title.strip():
        ny_oppgave = {
            "id": str(uuid.uuid4()),
            "tittel": new_title,
            "prosent": 0,
            "venter_pa": venter_pa if st.session_state["new_wait"] else ""
        }
        data["oppgaver"].append(ny_oppgave)
        save_data(data)
        st.success("✅ Oppgave lagt til!")
        st.session_state["new_title"] = ""
        st.session_state["wait_toggle"] = False
        st.session_state["venter_pa_input"] = ""
        st.experimental_rerun()
    else:
        st.warning("Du må skrive en tittel for oppgaven.")
