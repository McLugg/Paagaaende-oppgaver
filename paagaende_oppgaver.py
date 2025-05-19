import streamlit as st
import json
import os

# Constants
DATA_FILE = "tasks.json"

# --- Data persistence helpers ---
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# --- Utility functions ---
def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def complete_task(task_id):
    # Remove task and persist
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]
    save_tasks(st.session_state.tasks)
    st.experimental_rerun()

# --- Initialize session state ---
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# --- Page setup ---
st.set_page_config(page_title="Mine oppgaver", layout="centered")
st.title("✅ Mine oppgaver")

# --- Metrics ---
total = len(st.session_state.tasks)
done = 0  # We delete completed tasks, so always 0
avg_time = "-"
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", total)
col2.metric("Ferdig", done)
col3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# --- Display ongoing tasks ABOVE form ---
st.markdown("🔍 **Pågående oppgaver**")
for task in st.session_state.tasks:
    percent = task.get("progress", 0)
    emoji = " 🙉" if task.get("wait_for") else ""
    header = f"{task['title']} — {percent}%{emoji}"
    with st.expander(header):
        st.write(task.get("desc", ""))
        if task.get("wait_for"):
            st.warning(f"Venter på: {task['wait_for']}")
        # Progress slider
        new_val = st.slider(
            "Fremdrift (%)", min_value=0, max_value=100,
            value=percent, key=f"progress_{task['id']}")
        if new_val != percent:
            task["progress"] = new_val
            save_tasks(st.session_state.tasks)
            st.experimental_rerun()
        # Complete button
        if st.button("✔️ Fullfør", key=f"done_{task['id']}", on_click=complete_task, args=(task['id'],)):
            pass  # callback handles rerun

st.markdown("---")

# --- Add new task form BELOW tasks ---
with st.expander("➕ Legg til ny oppgave", expanded=True):
    with st.form("new_task_form", clear_on_submit=True):
        title = st.text_input("Tittel")
        desc = st.text_area("Beskrivelse")
        wait_for = st.text_input("Kommentar: Hva venter du på?")
        submit = st.form_submit_button("Legg til oppgave")

        if submit:
            if not title.strip():
                st.error("❌ Tittel kan ikke være tom.")
            elif total >= 10:
                st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
            else:
                new_id = get_next_id(st.session_state.tasks)
                new_task = {
                    "id": new_id,
                    "title": title,
                    "desc": desc,
                    "wait_for": wait_for.strip(),
                    "progress": 0
                }
                st.session_state.tasks.append(new_task)
                save_tasks(st.session_state.tasks)
                st.success("🚀 Ny oppgave registrert!")
                st.experimental_rerun()
