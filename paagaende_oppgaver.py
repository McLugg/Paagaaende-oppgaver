
import streamlit as st

st.set_page_config(page_title="Mine oppgaver", layout="centered")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Callback for å legge til
def add_task():
    if not st.session_state.title:
        st.error("❌ Tittel kan ikke være tom.")
        return
    if len(st.session_state.tasks) >= 10:
        st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
        return
    st.session_state.tasks.append({
        "title": st.session_state.title,
        "desc": st.session_state.desc,
        "wait": st.session_state.wait,
        "wait_for": st.session_state.wait_for if st.session_state.wait else "",
        "progress": 0
    })
    st.success("🚀 Ny oppgave registrert!")
    # Resett form-felt
    st.session_state.title = ""
    st.session_state.desc = ""
    st.session_state.wait = False
    st.session_state.wait_for = ""

# UI
st.title("✅ Mine oppgaver")

# Status
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"
c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total)
c2.metric("Ferdig", done)
c3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# Legg til oppgave i form
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
        if task["wait"]:
            st.warning(f"Venter på: {task['wait_for']}")
        p = st.slider("Fremdrift (%)",
                      min_value=0, max_value=100,
                      value=task["progress"],
                      key=f"prog_{i}")
        task["progress"] = p
        st.progress(p/100, text=f"{p}%")
        if p == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
            show_insp()
