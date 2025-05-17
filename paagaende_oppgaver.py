
import streamlit as st
import json
import os
import uuid

DATA_FILE = "data.json"

# Last ned og last opp JSON-data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"oppgaver": [], "fullfort": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Init session_state for nødvendige felt
for key in ["new_title", "new_wait", "new_comment"]:
    if key not in st.session_state:
        st.session_state[key] = ""

if "prosent" not in st.session_state:
    st.session_state["prosent"] = 0

data = load_data()
st.title("Oppgaveliste")

# PÅGÅENDE OPPGAVER FØRST
st.header("Pågående oppgaver")
for o in data["oppgaver"]:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"**{o['title']}**")
        if o.get("venter_paa"):
            st.caption(f"Venter på: {o['kommentar']}")
        # Slider for fremdrift
        key = f"slider_{o['id']}"
        prosent = st.slider("Fremdrift", 0, 100, o.get("prosent", 0), key=key)
        if prosent != o.get("prosent", 0):
            o["prosent"] = prosent
            save_data(data)
            st.rerun()
    with col2:
        if st.button("✔️ Fullført", key=f"done_{o['id']}"):
            data["oppgaver"].remove(o)
            data["fullfort"].append(o)
            save_data(data)
            st.rerun()

# LEGG TIL OPPGAVE
st.header("Legg til ny oppgave")
with st.form(key="new_task_form"):
    st.text_input("Tittel", key="new_title")
    st.checkbox("Venter på noen?", key="new_wait")
    if st.session_state.new_wait:
        st.text_input("Hva venter du på?", key="new_comment")
    submitted = st.form_submit_button("Legg til")
    if submitted and st.session_state.new_title:
        ny_oppgave = {
            "id": str(uuid.uuid4()),
            "title": st.session_state.new_title,
            "venter_paa": st.session_state.new_wait,
            "kommentar": st.session_state.new_comment if st.session_state.new_wait else "",
            "prosent": 0,
        }
        data["oppgaver"].append(ny_oppgave)
        save_data(data)
        st.session_state.new_title = ""
        st.session_state.new_wait = False
        st.session_state.new_comment = ""
        st.rerun()

# FULLFØRTE OPPGAVER
if data["fullfort"]:
    st.header("Fullførte oppgaver ✅")
    for f in data["fullfort"]:
        st.write(f"- {f['title']}")
