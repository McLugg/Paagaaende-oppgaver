import streamlit as st
import os
import json

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
total = len(tasks)
done = sum(1 for t in tasks if t.get("progress") == 100)
avg_time = "-"
c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total)
c2.metric("Ferdig", done)
c3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# Function to save tasks
def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

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
            elif total >= 10:
                st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
            else:
                new_task = {
                    "title": title,
                    "desc": desc,
                    "wait_for": wait_for.strip(),
                    "progress": 0
                }
                tasks.append(new_task)
                save_tasks()
                st.success("🚀 Ny oppgave registrert!")

st.markdown("---")
st.markdown("🔍 **Pågående oppgaver**")

# Display tasks
for idx, task in enumerate(tasks):
    header = f"{task['title']} — {task.get('progress', 0)}%{' 🙉' if task.get('wait_for') else ''}"
    with st.expander(header):
        st.write(task["desc"])
        if task.get("wait_for"):
            st.warning(f"Venter på: {task['wait_for']}")
        # Progress slider
        progress = st.slider("Fremdrift (%)", 0, 100, task.get("progress", 0), key=f"prog_{idx}")
        if progress != task.get("progress", 0):
            task["progress"] = progress
            save_tasks()
        # Custom arcade-style bar
        st.markdown(f"""
            <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
              <div style="
                background:#5FAA58;
                width:{progress}%;
                height:100%;
                transform:skew(-10deg);
                box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;
              "></div>
              <div style="
                position:absolute;top:0;left:0;width:100%;
                text-align:center;line-height:24px;
                font-family:'Press Start 2P',monospace;
                color:#FFF;font-size:12px;
              ">{progress}%</div>
            </div>
        """, unsafe_allow_html=True)
        if progress == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
