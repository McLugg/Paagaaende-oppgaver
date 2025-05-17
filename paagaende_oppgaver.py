
import streamlit as st
import json
import os
import uuid
from datetime import datetime

st.set_page_config(page_title="Felles Oppgaveliste", layout="centered")

DATA_FILE = "oppgaver.json"
MAX_OPPGAVER = 10
BAR_COLOR = "#5FAA58"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"oppgaver": [], "fullfort": []}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

st.title("📝 Mine Oppgaver")

# Pågående oppgaver øverst
st.header("📌 Pågående oppgaver")

for o in data["oppgaver"]:
    st.subheader(o["tittel"])
    if o.get("venter_pa"):
        st.markdown(f"⏳ *Venter på:* {o['venter_pa']}")
    prosent = st.slider(
        "Fremdrift", 0, 100, o["status"], key=f"slider_{o['id']}", 
        format="%d%%"
    )
    if prosent != o["status"]:
        o["status"] = prosent
        if prosent == 100:
            st.success("🎉 Oppgave fullført! Du rocker!")
            data["fullfort"].append({**o, "ferdig_tid": str(datetime.now())})
            data["oppgaver"] = [x for x in data["oppgaver"] if x["id"] != o["id"]]
            save_data(data)
            st.experimental_rerun()
    progress_width = int(prosent * 2)
    bar_html = f"""
    <div style='background-color: #ccc; width: 200px; height: 25px; border-radius: 6px;'>
        <div style='background-color: {BAR_COLOR}; width: {progress_width}px; height: 25px; border-radius: 6px;'></div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)
    st.write("---")

# Legge til oppgaver nederst
st.header("➕ Legg til ny oppgave")

with st.form("ny_oppgave"):
    new_title = st.text_input("Oppgavetittel", key="new_title")
    new_description = st.text_area("Beskrivelse", key="new_description")
    new_wait = st.checkbox("Venter på noen?", key="new_wait")
    new_wait_text = ""
    if new_wait:
        new_wait_text = st.text_input("Hvem venter du på?", key="new_wait_text")

    submitted = st.form_submit_button("Legg til")

    if submitted:
        if len(data["oppgaver"]) >= MAX_OPPGAVER:
            st.warning("🚫 Maks 10 oppgaver. Fullfør noen før du legger til flere!")
        elif not new_title.strip():
            st.warning("⚠️ Oppgaven må ha en tittel.")
        else:
            data["oppgaver"].append({
                "id": str(uuid.uuid4()),
                "tittel": new_title.strip(),
                "beskrivelse": new_description.strip(),
                "venter_pa": new_wait_text.strip() if new_wait else "",
                "status": 0
            })
            save_data(data)
            st.success("✅ Oppgave lagt til!")
            st.experimental_rerun()

# KPI
st.header("📊 KPI")
totalt = len(data["oppgaver"]) + len(data["fullfort"])
fullfort = len(data["fullfort"])
snitt_tid = "-"
if data["fullfort"]:
    tider = []
    for o in data["fullfort"]:
        try:
            start = datetime.fromisoformat(o["start_tid"])
            ferdig = datetime.fromisoformat(o["ferdig_tid"])
            tider.append((ferdig - start).total_seconds())
        except:
            pass
    if tider:
        snitt_tid = f"{sum(tider)/len(tider):.1f} sekunder"
st.write(f"- Antall oppgaver: {len(data['oppgaver'])}")
st.write(f"- Fullført: {fullfort}")
st.write(f"- Snitt tid: {snitt_tid}")
