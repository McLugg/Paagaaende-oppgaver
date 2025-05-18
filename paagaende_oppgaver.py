import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="Mine oppgaver", layout="centered")

DATA_FILE = "tasks.json"

# Load tasks from JSON file
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            tasks = []
else:
    tasks = []

# Title and KPIs
st.title("✅ Mine oppgaver")

# Compute average duration if stored
durations_file = "durations.json"
if os.path.exists(durations_file):
    with open(durations_file, "r") as f:
        try:
            durations = json.load(f)
        except json.JSONDecodeError:
            durations = []
else:
    durations = []

total = len(tasks)
done = sum(1 for t in tasks if t.get("progress") == 100)
# avg_time placeholder (not yet tracking)
avg_time = "-"
if durations:
    avg_time = f"{round(sum(durations)/len(durations),1)} min"
c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total + len(durations))
c2.metric("Ferdig", len(durations))
c3.metric("Snitt tid", avg_time)
st.markdown("---")

# Save helper
def save_all():
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
    with open(durations_file, "w") as f:
        json.dump(durations, f, indent=2)

# Display ongoing tasks
st.markdown("## 🔍 Pågående oppgaver")
for idx, task in enumerate(tasks.copy()):
    percent = task.get("progress", 0)
    emoji = " 🙉" if task.get("wait_for") else ""
    header = f"{task['title']} — {percent}%{emoji}"
    with st.expander(header):
        st.write(task["desc"])
        if task.get("wait_for"):
            st.warning(f"Venter på: {task['wait_for']}")
        p = st.slider(
            "Fremdrift (%)", 0, 100, percent, key=f"prog_{idx}"
        )
        if p != task.get("progress", 0):
            task["progress"] = p
            if p == 100:
                # record duration if created_at in task
                created = task.get("created_at")
                if created:
                    duration = (datetime.now().timestamp() - created) / 60
                    durations.append(duration)
                # remove completed task
                tasks.pop(idx)
            save_all()
            st.experimental_rerun()

        # Custom arcade-style bar
        st.markdown(f"""
            <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
              <div style="
                background:#5FAA58;
                width:{p}%;
                height:100%;
                transform:skew(-10deg);
                box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;
              "></div>
              <div style="
                position:absolute;top:0;left:0;width:100%;
                text-align:center;line-height:24px;
                font-family:'Press Start 2P',monospace;
                color:#FFF;font-size:12px;
              ">{p}%</div>
            </div>
        """, unsafe_allow_html=True)

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
            elif len(tasks) >= 10:
                st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
            else:
                new_task = {
                    "title": title,
                    "desc": desc,
                    "wait_for": wait_for.strip(),
                    "progress": 0,
                    "created_at": datetime.now().timestamp()
                }
                tasks.append(new_task)
                save_all()
                st.success("🚀 Ny oppgave registrert!")
