import streamlit as st
import os
import json

st.set_page_config(page_title="Mine oppgaver", layout="centered")

# Initialiser session state og last inn oppgaver hvis lagret
if "tasks" not in st.session_state:
    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r") as f:
                st.session_state.tasks = json.load(f)
        except:
            st.session_state.tasks = []
    else:
        st.session_state.tasks = []

# Callback for å legge til ny oppgave
def add_task():
    if not st.session_state.title:
        st.error("❌ Tittel kan ikke være tom.")
        return
    if len(st.session_state.tasks) >= 10:
        st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
        return
    # Opprett nytt oppgave-objekt
    task = {
        "title": st.session_state.title,
        "desc": st.session_state.desc,
        "wait": st.session_state.wait,
        "progress": 0
    }
    # Kun inkluder 'wait_for' hvis brukeren har fylt inn noe
    if st.session_state.wait and str(st.session_state.wait_for).strip() != "":
        task["wait_for"] = st.session_state.wait_for
    st.session_state.tasks.append(task)
    st.success("🚀 Ny oppgave registrert!")
    # Resett form-felt
    st.session_state.title = ""
    st.session_state.desc = ""
    st.session_state.wait = False
    st.session_state.wait_for = ""
    # Lagre oppgaver til JSON-fil
    with open("tasks.json", "w") as f:
        json.dump(st.session_state.tasks, f)

# UI
st.title("✅ Mine oppgaver")

# Status
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t.get("progress") == 100)
avg_time = "-"
c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total)
c2.metric("Ferdig", done)
c3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# Legg til oppgave
with st.form(key="task_form"):
    st.markdown("### ➕ Legg til ny oppgave")
    st.text_input("Tittel", key="title")
    st.text_area("Beskrivelse", key="desc")
    st.checkbox("Venter på noen?", key="wait")
    if st.session_state.wait:
        st.text_input("Kommentar: Hva venter du på?", key="wait_for")
    st.form_submit_button("Legg til oppgave", on_click=add_task)

st.markdown("---")
st.markdown("## 🔍 Pågående oppgaver")

# Vis oppgaver
def show_insp():
    st.balloons()

for i, task in enumerate(st.session_state.tasks):
    with st.expander(task["title"]):
        st.write(task["desc"])
        if task.get("wait"):
            if task.get("wait_for"):
                st.warning(f"Venter på: {task['wait_for']}")
            else:
                st.warning("Venter på: (ingen kommentar)")
        p = st.slider("Fremdrift (%)", min_value=0, max_value=100,
                      value=task["progress"], key=f"prog_{i}")
        task["progress"] = p
        st.progress(p/100, text=f"{p}%")
        if p == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
            show_insp()

# Lagre oppgaver til JSON etter endringer (f.eks. fremdrift)
with open("tasks.json", "w") as f:
    json.dump(st.session_state.tasks, f)
