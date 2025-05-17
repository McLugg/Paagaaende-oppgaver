
import streamlit as st
import json
import os
import uuid

st.set_page_config(page_title="Oppgaveoversikt", layout="centered")

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"oppgaver": [], "fullfort": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

st.title("📝 Pågående Oppgaver")

# Vise pågående oppgaver øverst
st.subheader("📋 Pågående oppgaver")
for o in data["oppgaver"]:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"**{o['tittel']}**")
        if o.get("venter"):
            st.caption(f"⏳ Venter på: {o.get('kommentar', '')}")
    with col2:
        prosent = st.slider("Fremdrift", 0, 100, o["prosent"], key=f"slider_{o['id']}", format="%d%%")
        if prosent != o["prosent"]:
            o["prosent"] = prosent
            if prosent == 100:
                data["oppgaver"].remove(o)
                data["fullfort"].append(o)
                st.success("🎉 Oppgave fullført! Du er en legende!")
                save_data(data)
                st.experimental_rerun()
save_data(data)

# Deretter legge til ny oppgave
st.subheader("➕ Legg til ny oppgave")
with st.form("ny_oppgave"):
    tittel = st.text_input("Oppgavetittel", key="new_title")
    venter = st.checkbox("Venter på noen?", key="new_wait")
    kommentar = ""
    if venter:
        kommentar = st.text_area("Hva venter du på?", key="new_comment")
    submitted = st.form_submit_button("Legg til oppgave")
    if submitted and tittel.strip() != "":
        ny = {
            "id": str(uuid.uuid4()),
            "tittel": tittel,
            "venter": venter,
            "kommentar": kommentar,
            "prosent": 0
        }
        data["oppgaver"].append(ny)
        save_data(data)
        st.experimental_rerun()

# Vise fullførte oppgaver
st.subheader("✅ Fullførte oppgaver")
for f in data["fullfort"]:
    st.markdown(f"- {f['tittel']} (100%)")
