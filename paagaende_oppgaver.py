
import streamlit as st
import json
import os
from datetime import datetime

# Path to data file
DATA_PATH = "data.json"

def load_data():
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"tasks": []}
    return {"tasks": []}

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="Mine oppgaver", layout="centered")
st.title("✅ Mine oppgaver")

# Load tasks
data = load_data()
tasks = data.get("tasks", [])

# KPI section
total = len(tasks)
completed_tasks = [t for t in tasks if t.get("progress", 0) == 100]
done = len(completed_tasks)
times = []
for t in completed_tasks:
    if t.get("created_at") and t.get("completed_at"):
        start = datetime.fromisoformat(t["created_at"])
        end = datetime.fromisoformat(t["completed_at"])
        times.append((end - start).total_seconds() / 60)
avg = f"{round(sum(times)/len(times),1)} min" if times else "-"

c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total)
c2.metric("Ferdig", done)
c3.metric("Snitt tid", avg)

st.markdown("---")

# Form to add a new task
with st.form("add_task_form", clear_on_submit=True):
    st.subheader("➕ Legg til ny oppgave")
    title = st.text_input("Tittel")
    desc = st.text_area("Beskrivelse")
    wait = st.checkbox("Venter på noen?")
    comment = ""
    if wait:
        comment = st.text_input("Hva venter du på?", max_chars=50)
    submitted = st.form_submit_button("Legg til oppgave")
    if submitted:
        if not title.strip():
            st.error("❌ Tittel kan ikke være tom.")
        elif total >= 10:
            st.error("🚫 Maks 10 oppgaver nådd. Fullfør noen først.")
        else:
            now = datetime.now().isoformat()
            new_task = {
                "id": datetime.now().timestamp(),
                "title": title,
                "description": desc,
                "wait": wait,
                "comment": comment,
                "progress": 0,
                "created_at": now,
                "completed_at": ""
            }
            tasks.append(new_task)
            data["tasks"] = tasks
            save_data(data)
            st.success("✅ Oppgave lagt til!")

st.markdown("---")
st.subheader("🔍 Pågående oppgaver")
for t in tasks:
    if t.get("progress", 0) < 100:
        with st.expander(t["title"], expanded=False):
            st.write(t["description"])
            if t.get("wait"):
                st.info(f"⚠️ Venter på: {t['comment']}")
            prog = st.slider(
                "Fremdrift (%)", 0, 100, t.get("progress", 0),
                step=1, key=f"prog_{t['id']}"
            )
            if prog != t.get("progress", 0):
                t["progress"] = prog
                if prog == 100:
                    t["completed_at"] = datetime.now().isoformat()
                    st.success("🎉 Oppgave fullført!")
                save_data(data)
            st.progress(t["progress"]/100)
