
import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "data.json"

# --- Helper functions ---
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f).get("tasks", [])
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump({"tasks": tasks}, f, default=str, indent=2)

def display_kpi(tasks):
    total = len(tasks)
    done_tasks = [t for t in tasks if t.get("progress", 0) == 100]
    completed = len(done_tasks)
    # Calculate average time in minutes
    times = []
    for t in done_tasks:
        try:
            ct = datetime.fromisoformat(t["completed_at"])
            stt = datetime.fromisoformat(t["created_at"])
            times.append((ct - stt).total_seconds() / 60)
        except:
            pass
    avg = round(sum(times)/len(times), 1) if times else "-"
    c1, c2, c3 = st.columns(3)
    c1.metric("Oppgaver totalt", total)
    c2.metric("Ferdig", completed)
    c3.metric("Snitt tid", f"{avg} min" if isinstance(avg, float) else "-")

# --- Main ---
st.set_page_config(page_title="Mine oppgaver")

# Initialize session state
for key in ("tasks", "new_title", "new_desc", "new_wait", "new_waiting_on"):
    if key not in st.session_state:
        st.session_state[key] = "" if key != "tasks" else load_tasks()

st.title("✅ Mine oppgaver")

# KPI
display_kpi(st.session_state.tasks)
st.markdown("---")

# Add new task
with st.expander("➕ Legg til ny oppgave", expanded=True):
    st.text_input("Tittel", key="new_title")
    st.text_area("Beskrivelse", key="new_desc")
    st.checkbox("Venter på noen?", key="new_wait")
    if st.session_state.new_wait:
        st.text_input("Hva venter du på?", key="new_waiting_on")
    if st.button("Legg til oppgave"):
        if len(st.session_state.tasks) >= 10:
            st.error("Du kan ikke legge til mer enn 10 oppgaver, fullfør noen først!")
        else:
            task = {
                "id": datetime.now().timestamp(),
                "title": st.session_state.new_title,
                "desc": st.session_state.new_desc,
                "waiting": bool(st.session_state.new_wait),
                "waiting_on": st.session_state.new_waiting_on if st.session_state.new_wait else "",
                "progress": 0,
                "created_at": datetime.now().isoformat(),
                "completed_at": ""
            }
            st.session_state.tasks.append(task)
            save_tasks(st.session_state.tasks)
            # Reset inputs
            st.session_state.new_title = ""
            st.session_state.new_desc = ""
            st.session_state.new_wait = False
            st.session_state.new_waiting_on = ""
            st.success("🚀 Ny oppgave registrert!")
            st.experimental_rerun()

st.markdown("---")

# Display tasks
st.header("🔍 Pågående oppgaver")
for t in st.session_state.tasks:
    with st.expander(t["title"], expanded=False):
        if t.get("waiting"):
            st.info(f"⚠️ Venter på: {t['waiting_on']}")
        val = st.slider(
            "Fremdrift (%)",
            min_value=0,
            max_value=100,
            value=int(t.get("progress", 0)),
            key=f"slider_{t['id']}"
        )
        if val != t.get("progress", 0):
            t["progress"] = val
            if val == 100:
                t["completed_at"] = datetime.now().isoformat()
                st.success("🎉 Fantastisk! Oppgaven er fullført!")
            save_tasks(st.session_state.tasks)
            st.experimental_rerun()
        st.progress(t["progress"]/100)
