
import streamlit as st
import json
import os
from datetime import datetime
import random
import uuid

DATA_PATH = "data.json"

def load_data():
    if not os.path.exists(DATA_PATH):
        return {"oppgaver": [], "fullfort": []}
    with open(DATA_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    data.setdefault("oppgaver", [])
    data.setdefault("fullfort", [])
    return data

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

# session state defaults
for key, default in [("tittel",""),("beskrivelse",""),("venter",False),("kommentar","")]:
    if key not in st.session_state:
        st.session_state[key] = default

st.set_page_config(page_title="Mine oppgaver", layout="centered")
st.title("✅ Mine oppgaver")

data = load_data()
oppgaver = data["oppgaver"]
fullfort = data["fullfort"]

# KPI
st.subheader("📊 Status")
totalt = len(oppgaver) + len(fullfort)
ferdig = len(fullfort)
if ferdig > 0:
    tider=[]
    for o in fullfort:
        if "start_tid" in o and "ferdig_tid" in o:
            start=datetime.fromisoformat(o["start_tid"])
            end=datetime.fromisoformat(o["ferdig_tid"])
            tider.append((end-start).total_seconds())
    snitt = f"{round(sum(tider)/len(tider)/60,1)} min" if tider else "-"
else:
    snitt="-"
c1,c2,c3=st.columns(3)
c1.metric("Oppgaver totalt",totalt)
c2.metric("Ferdig",ferdig)
c3.metric("Snitt tid",snitt)

st.markdown("---")
st.subheader("➕ Legg til ny oppgave")
tittel = st.text_input("Tittel", key="tittel")
beskrivelse = st.text_area("Beskrivelse", key="beskrivelse")
venter = st.checkbox("Venter på noen?", key="venter")
kommentar=""
if venter:
    kommentar = st.text_input("Hva venter du på?", key="kommentar")

if st.button("Legg til oppgave"):
    if not tittel.strip():
        st.error("❌ Tittel kan ikke være tom.")
    elif len(oppgaver)>=10:
        st.warning("🚫 Maks 10 oppgaver. Fullfør noen først.")
    else:
        ny={
            "id": uuid.uuid4().hex,
            "tittel": tittel,
            "beskrivelse": beskrivelse,
            "status": 0,
            "start_tid": datetime.now().isoformat(),
            "venter": venter,
            "kommentar": kommentar
        }
        oppgaver.append(ny)
        save_data(data)
        st.success(random.choice(["📝 Klar for innsats!","🚀 Ny oppgave registrert!","✅ Oppgave lagt til!"]))
        # reset
        st.session_state.tittel=""
        st.session_state.beskrivelse=""
        st.session_state.venter=False
        st.session_state.kommentar=""

st.markdown("---")
st.subheader("🔍 Pågående oppgaver")
for o in list(oppgaver):
    with st.expander(o["tittel"]):
        st.write(o["beskrivelse"])
        if o.get("venter"):
            st.info(f"⚠️ Venter på: {o.get('kommentar','')}")
        # ensure status is int
        stat = o.get("status",0)
        try:
            stat = int(stat)
        except:
            stat = 0
        # slider
        key=f"slider_{o['id']}"
        procent = st.slider(
            label="",
            min_value=0, max_value=100,
            value=stat, step=10,
            key=key, label_visibility="collapsed"
        )
        o["status"]=procent
        # custom bar
        bar = f"""<div style="background:#eee;border-radius:8px;overflow:hidden;">
            <div style="width:{procent}%;background:#5FAA58;padding:4px 0;text-align:center;color:white;font-weight:bold;">
            {procent}%
            </div></div>"""
        st.markdown(bar, unsafe_allow_html=True)
        if procent>=100:
            o["ferdig_tid"]=datetime.now().isoformat()
            fullfort.append(o)
            oppgaver.remove(o)
            save_data(data)
            st.balloons()
            st.success(random.choice(["🎉 Fantastisk jobba!","👏 Bra jobbet!","🏆 Oppgave fullført!"]))
