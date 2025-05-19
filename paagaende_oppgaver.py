import streamlit as st
import json
import os

st.set_page_config(page_title="Mine oppgaver", layout="centered")

DATA_FILE = "tasks.json"

# Load tasks from JSON (persist across refresh)
if "tasks" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.tasks = json.load(f)
    else:
        st.session_state.tasks = []

# Title and status metrics
st.title("✅ Mine oppgaver")
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"  # Placeholder for future time tracking
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", total)
col2.metric("Ferdig", done)
col3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# Display ongoing tasks first
st.markdown("🔍 **Pågående oppgaver**")
to_remove = []
for idx, task in enumerate(st.session_state.tasks):
    percent = task["progress"]
    emoji = " 🙉" if task.get("wait_for") else ""
    header = f"{task['title']} — {percent}%{emoji}"
    with st.expander(header):
        st.write(task.get("desc", ""))
        if task.get("wait_for"):
            st.warning(f"Venter på: {task['wait_for']}")
        new_progress = st.slider(
            "Fremdrift (%)", 0, 100,
            value=percent, key=f"progress_{idx}"
        )
        if new_progress != percent:
            task["progress"] = new_progress
            with open(DATA_FILE, "w") as f:
                json.dump(st.session_state.tasks, f)
        st.markdown(f"""
            <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
              <div style="background:#5FAA58;width:{task['progress']}%;height:100%;transform:skew(-10deg);box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;"></div>
              <div style="position:absolute;top:0;left:0;width:100%;text-align:center;line-height:24px;font-family:'Press Start 2P',monospace;color:#FFF;font-size:12px;">{task['progress']}%</div>
            </div>
        """, unsafe_allow_html=True)
        if task["progress"] == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
            to_remove.append(task)

# Remove completed tasks
if to_remove:
    for t in to_remove:
        st.session_state.tasks.remove(t)
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.tasks, f)

st.markdown("---")

# Add new task form
with st.expander("➕ Legg til ny oppgave", expanded=True):
    with st.form("new_task_form", clear_on_submit=True):
        title = st.text_input("Tittel")
        desc = st.text_area("Beskrivelse")
        wait_for = st.text_input("Kommentar: Hva venter du på?")
        submit = st.form_submit_button("Legg til oppgave")

        if submit:
            if not title:
                st.error("❌ Tittel kan ikke være tom.")
            elif len(st.session_state.tasks) >= 10:
                st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
            else:
                new_task = {
                    "title": title,
                    "desc": desc,
                    "wait_for": wait_for.strip(),
                    "progress": 0
                }
                st.session_state.tasks.append(new_task)
                with open(DATA_FILE, "w") as f:
                    json.dump(st.session_state.tasks, f)
                st.success("🚀 Ny oppgave registrert!")
