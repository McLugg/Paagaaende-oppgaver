import streamlit as st, json, os, uuid

DATA_FILE = "tasks.json"

def load_tasks():
    try:
        return json.load(open(DATA_FILE))
    except:
        return []

def save_tasks(tasks):
    json.dump(tasks, open(DATA_FILE, "w"))

def add_task():
    new = {
        "id":       str(uuid.uuid4()),
        "title":    st.session_state.title_in.strip(),
        "desc":     st.session_state.desc_in.strip(),
        "wait_for": st.session_state.wait_in.strip(),
        "progress": 0,
    }
    st.session_state.tasks.append(new)
    save_tasks(st.session_state.tasks)
    st.experimental_rerun()

def complete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]
    save_tasks(st.session_state.tasks)
    st.experimental_rerun()

# --- INIT ---
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# ... KPI ...

# --- PÅGÅENDE OPPGAVER ---
for task in st.session_state.tasks:
    header = f"{task['title']} — {task['progress']}% {'🙉' if task['wait_for'] else ''}"
    with st.expander(header):
        # ...
        if st.button("✔️ Fullfør", key=f"done_{task['id']}", on_click=complete_task, args=(task["id"],)):
            pass

# --- LEGG TIL OPPGAVE ---
st.text_input("Tittel", key="title_in")
st.text_area("Beskrivelse", key="desc_in")
st.text_input("Kommentar: Hva venter du på?", key="wait_in")
st.button("Legg til oppgave", on_click=add_task)
