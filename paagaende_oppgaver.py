
import streamlit as st
import json
import uuid
import os

DATAFIL = "oppgaver.json"

def last_data():
    if not os.path.exists(DATAFIL):
        with open(DATAFIL, "w") as f:
            json.dump({"oppgaver": [], "fullfort": []}, f)
    with open(DATAFIL, "r") as f:
        return json.load(f)

def lagre_data(data):
    with open(DATAFIL, "w") as f:
        json.dump(data, f, indent=4)

st.set_page_config(page_title="Pågående Oppgaver", layout="centered")
st.title("✅ Pågående Oppgaver")

data = last_data()

st.subheader("Legg til ny oppgave")

st.text_input("Tittel", key="new_title")
st.text_area("Beskrivelse", key="new_description")
st.checkbox("Venter på noen?", key="new_wait")

if st.session_state.get("new_wait"):
    st.text_input("Kommentar: Hva venter du på?", key="new_comment")

if st.button("Legg til oppgave"):
    ny_oppgave = {
        "id": str(uuid.uuid4()),
        "tittel": st.session_state.new_title,
        "beskrivelse": st.session_state.new_description,
        "venter": st.session_state.new_wait,
        "kommentar": st.session_state.new_comment if st.session_state.new_wait else "",
        "prosent": 0
    }
    data["oppgaver"].append(ny_oppgave)
    lagre_data(data)

    for key in ["new_title", "new_description", "new_wait", "new_comment"]:
        if key in st.session_state:
            del st.session_state[key]

    st.experimental_rerun()

st.subheader("Pågående oppgaver")

for o in data["oppgaver"]:
    st.markdown(f"### {o['tittel']}")
    st.write(o["beskrivelse"])
    if o.get("venter") and o.get("kommentar"):
        st.info(f"🔄 Venter på: {o['kommentar']}")
    percent_key = f"slider_{o['id']}"
    prosent = st.slider("Fremdrift", 0, 100, o["prosent"], key=percent_key)
    if prosent != o["prosent"]:
        o["prosent"] = prosent
        lagre_data(data)
        if prosent == 100:
            data["oppgaver"] = [x for x in data["oppgaver"] if x["id"] != o["id"]]
            data["fullfort"].append(o)
            lagre_data(data)
            st.experimental_rerun()
