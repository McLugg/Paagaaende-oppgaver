
import streamlit as st
import json
import os
import time
from datetime import datetime

DATA_FILE = "tasks.json"

# Load or initialize storage
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)
with open(DATA_FILE, "r") as f:
    tasks = json.load(f)

st.title("✅ Mine oppgaver")

# Status KPI
total = len(tasks)
done = sum(1 for t in tasks if t["progress"] >= 100)
times = [t.get("duration", 0) for t in tasks if t.get("duration", 0) > 0]
avg = sum(times)/len(times) if times else None
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", total)
col2.metric("Ferdig", done)
col3.metric("Snitt tid", f"{avg:.1f} min" if avg else "-")

st.markdown("---")

# Add new task
with st.expander("➕ Legg til ny oppgave", True):
    title = st.text_input("Tittel")
    desc = st.text_area("Beskrivelse")
    wait = st.checkbox("Venter på noen?")
    who = ""
    if wait:
        who = st.text_input("Hva venter du på?")
    if st.button("Legg til oppgave"):
        if total >= 10:
            st.error("🎉 Maks 10 oppgaver! Fullfør noen før du legger til flere.")
        elif not title:
            st.warning("Gi oppgaven en tittel.")
        else:
            new = {
                "id": int(time.time()*1000),
                "title": title,
                "desc": desc,
                "wait": wait,
                "who": who,
                "progress": 0,
                "created": datetime.now().isoformat()
            }
            tasks.append(new)
            with open(DATA_FILE, "w") as f:
                json.dump(tasks, f, indent=2)
            st.success("🚀 Ny oppgave registrert!")
            st.experimental_rerun()

st.markdown("---")

# Show tasks
st.header("🔍 Pågående oppgaver")
for t in tasks:
    key = f"task_{t['id']}"
    with st.expander(t["title"], False):
        if t["wait"]:
            st.info(f"⚠️ Venter på: {t['who']}")
        # slider for progress
        prog = st.slider("Fremdrift (%)", 0, 100, t["progress"], key=t["id"], format="%d%%")
        if prog != t["progress"]:
            t["progress"] = prog
            if prog == 100:
                t["duration"] = (time.time() - t["id"]/1000) / 60
                st.balloons()
                st.success("🎉 Oppgave fullført!")
            with open(DATA_FILE, "w") as f:
                json.dump(tasks, f, indent=2)
            st.experimental_rerun()
