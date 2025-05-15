
import streamlit as st
import json
import os
import random
from datetime import datetime

DATA_FILE = "data.json"
MAX_OPPGAVER = 10

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"oppgaver": [], "fullfort": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

def legg_til_oppgave(data, tittel, beskrivelse):
    data["oppgaver"].append({
        "tittel": tittel,
        "beskrivelse": beskrivelse,
        "status": [False]*10,
        "venter": False,
        "ventetekst": "",
        "startet": datetime.now().isoformat()
    })

def formater_tid(start, slutt):
    try:
        diff = datetime.fromisoformat(slutt) - datetime.fromisoformat(start)
        minutter = int(diff.total_seconds() // 60)
        return f"{minutter} min"
    except:
        return "-"

ai_fullfort = [
    "Boom! En mindre ting i livet ditt 💥",
    "Du fortjener en kaffe nå ☕️",
    "Oppgavelisten din jubler litt stille akkurat nå 👏",
    "Du er på gli – dette går veien 🚀",
    "Enda en oppgave knust som en sjef 💼"
]

ai_nekt = [
    "Hold hestene! Du må ri ferdig noen oppgaver før du skaper flere 🐎",
    "10 er grensen – resten må vente på tribunen 🧠",
    "Tøm før du fyller. Det gjelder både kopper og to-do-lister ☕️",
    "Du er for effektiv – rydd litt plass før neste raid 🧹"
]

data = load_data()
st.set_page_config(page_title="Mine oppgaver")
st.title("✅ Mine oppgaver")

# KPI
st.subheader("📊 Status")
totalt = len(data["oppgaver"]) + len(data["fullfort"])
fullfort = len(data["fullfort"])
snitt_tid = "-"
if data["fullfort"]:
    tider = [
        (datetime.fromisoformat(o["fullfortet"]) - datetime.fromisoformat(o["startet"])).total_seconds()
        for o in data["fullfort"]
    ]
    snitt_tid = f"{int(sum(tider)/60/len(tider))} min"

k1, k2, k3 = st.columns(3)
k1.metric("Oppgaver totalt", totalt)
k2.metric("Ferdig", fullfort)
k3.metric("Snitt tid", snitt_tid)

st.markdown("---")

# Liste opp aktive oppgaver
nye = []
for idx, oppgave in enumerate(data["oppgaver"]):
    st.markdown(f"**{oppgave['tittel']}**")
    st.markdown(oppgave["beskrivelse"])

    cols = st.columns(10)
    for i in range(10):
        label = "✅" if oppgave["status"][i] else "⬜️"
        oppgave["status"][i] = cols[i].checkbox(label, value=oppgave["status"][i], key=f"{idx}_{i}", label_visibility="collapsed")

    prosent = sum(oppgave["status"]) * 10
    st.markdown(f"""<div style="height: 8px; background-color: #5FAA58; width: {prosent}%; border-radius: 6px; margin-top: 5px; margin-bottom: 10px;"></div>""", unsafe_allow_html=True)

    if oppgave["venter"]:
        st.warning(f"⚠️ Venter: {oppgave['ventetekst']}")

    if sum(oppgave["status"]) == 10:
        oppgave["fullfortet"] = datetime.now().isoformat()
        data["fullfort"].append(oppgave)
        st.success(random.choice(ai_fullfort))
    else:
        nye.append(oppgave)

    st.markdown("---")
data["oppgaver"] = nye

# Legg til ny oppgave nederst
if len(data["oppgaver"]) < MAX_OPPGAVER:
    with st.form("ny_oppgave"):
        st.subheader("➕ Legg til ny oppgave")
        tittel = st.text_input("Tittel")
        beskrivelse = st.text_area("Beskrivelse")
        vent = st.checkbox("Venter på noen?", key="venter_ny")
        kommentar = ""
        if vent:
            kommentar = st.text_input("Kort kommentar", max_chars=30)

        submitted = st.form_submit_button("Legg til")
        if submitted and tittel:
            legg_til_oppgave(data, tittel, beskrivelse)
            data["oppgaver"][-1]["venter"] = vent
            data["oppgaver"][-1]["ventetekst"] = kommentar
            st.success("✅ Oppgave lagt til!")
else:
    st.error(random.choice(ai_nekt))

save_data(data)
