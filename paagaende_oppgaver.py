import streamlit as st
import json, os

DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)

def add_task():
    """Kalles når brukeren klikker knappen."""
    title    = st.session_state["ti"].strip()
    desc     = st.session_state["de"].strip()
    wait_for = st.session_state["wf"].strip()
    # Validering
    if not title:
        st.error("❌ Tittel kan ikke være tom.")
        return
    if len(st.session_state.tasks) >= 10:
        st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
        return
    # Legg til
    st.session_state.tasks.append({
        "title":    title,
        "desc":     desc,
        "wait_for": wait_for,
        "progress": 0
    })
    save_tasks(st.session_state.tasks)
    # Tøm inputfelt
    st.session_state["ti"] = ""
    st.session_state["de"] = ""
    st.session_state["wf"] = ""
    st.success("🚀 Ny oppgave registrert!")

# --- INIT ---
st.set_page_config(page_title="Mine oppgaver", layout="centered")
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# --- HEADER + KPI ---
st.title("✅ Mine oppgaver")
total = len(st.session_state.tasks)
done  = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"
c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total)
c2.metric("Ferdig", done)
c3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# --- PÅGÅENDE OPPGAVER ---
st.markdown("🔍 **Pågående oppgaver**")
to_remove = []
for idx, task in enumerate(st.session_state.tasks):
    hdr_emoji = " 🙉" if task["wait_for"] else ""
    hdr = f"{task['title']} — {task['progress']}%{hdr_emoji}"
    with st.expander(hdr):
        st.write(task["desc"])
        if task["wait_for"]:
            st.warning(f"Venter på: {task['wait_for']}")
        new_p = st.slider("Fremdrift (%)", 0, 100, value=task["progress"], key=f"slider_{idx}")
        if new_p != task["progress"]:
            task["progress"] = new_p
            save_tasks(st.session_state.tasks)
        # Slett fullført
        if task["progress"] == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
            to_remove.append(idx)
# Fjern fullførte bakerst først
for i in sorted(to_remove, reverse=True):
    st.session_state.tasks.pop(i)
    save_tasks(st.session_state.tasks)

st.markdown("---")

# --- LEGG TIL OPPGAVE (med on_click!) ---
with st.expander("➕ Legg til ny oppgave", expanded=True):
    st.text_input("Tittel", key="ti")
    st.text_area("Beskrivelse", key="de")
    st.text_input("Kommentar: Hva venter du på?", key="wf")
    st.button("Legg til oppgave", on_click=add_task, key="add_btn")
