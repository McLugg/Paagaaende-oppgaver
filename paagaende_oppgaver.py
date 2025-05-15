
import streamlit as st

st.set_page_config(page_title="Mine oppgaver", layout="centered")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
    st.session_state.next_id = 1

st.title("✅ Mine oppgaver")

# Status metrics
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t.get("progress", 0) == 100)
avg_time = "-"  # Placeholder

c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total)
c2.metric("Ferdig", done)
c3.metric("Snitt tid", avg_time)

st.divider()

# Form to add a new task
with st.expander("➕ Legg til ny oppgave", expanded=False):
    with st.form("task_form", clear_on_submit=True):
        title = st.text_input("Tittel")
        description = st.text_area("Beskrivelse")
        wait = st.checkbox("Venter på noen?")
        wait_for = ""
        if wait:
            wait_for = st.text_input("Hva venter du på?")
        submitted = st.form_submit_button("Legg til oppgave")
        if submitted:
            if len(st.session_state.tasks) >= 10:
                st.error("Du kan ikke legge til mer enn 10 oppgaver. Fullfør noen først!")
            elif not title.strip():
                st.error("Tittel kan ikke være tom.")
            else:
                new_task = {
                    "id": st.session_state.next_id,
                    "title": title.strip(),
                    "description": description.strip(),
                    "wait": wait,
                    "wait_for": wait_for.strip(),
                    "progress": 0,
                    "completed": False
                }
                st.session_state.tasks.append(new_task)
                st.session_state.next_id += 1
                st.success("🚀 Ny oppgave registrert!")

st.divider()

st.subheader("🔍 Pågående oppgaver")
for task in st.session_state.tasks:
    with st.expander(task["title"]):
        if task["wait"]:
            st.warning(f"⚠️ Venter på: {task['wait_for']}")
        # Slider for progress
        progress = st.slider(
            "Fremdrift (%)", min_value=0, max_value=100, value=task["progress"],
            key=f"progress_{task['id']}"
        )
        task["progress"] = progress
        if progress == 100 and not task.get("completed", False):
            task["completed"] = True
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
