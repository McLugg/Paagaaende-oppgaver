
import streamlit as st
import datetime

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
    st.session_state.next_id = 1

st.set_page_config(page_title="Mine oppgaver", layout="wide")

# Header
st.markdown("## ✅ Mine oppgaver")

# KPI metrics
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t['progress'] == 100)
avg_time = "-"
if done > 0:
    avg_time = round(sum(t['time'] for t in st.session_state.tasks if t['progress'] == 100) / done, 1)
cols = st.columns(3)
cols[0].metric("Oppgaver totalt", total)
cols[1].metric("Ferdig", done)
cols[2].metric("Snitt tid", f"{avg_time} min")

st.markdown("---")

# Form for new task
with st.expander("➕ Legg til ny oppgave", expanded=True):
    title = st.text_input("Tittel", key="new_title")
    desc = st.text_area("Beskrivelse", key="new_desc")
    wait = st.checkbox("Venter på noen?", key="new_wait")
    wait_for = ""
    if wait:
        wait_for = st.text_input("Hva venter du på?", key="new_wait_for")
    if st.button("Legg til oppgave"):
        if total >= 10:
            # Fun AI-generated warning
            st.warning("🛑 Du har allerede 10 oppgaver! Løs noen før du legger til flere.")
        else:
            st.session_state.tasks.append({
                'id': st.session_state.next_id,
                'title': title,
                'desc': desc,
                'wait': wait,
                'wait_for': wait_for,
                'progress': 0,
                'time': 0,
                'created': datetime.datetime.now()
            })
            st.session_state.next_id += 1
            st.success("🚀 Ny oppgave registrert!")
            # Reset form fields
            st.session_state.new_title = ""
            st.session_state.new_desc = ""
            st.session_state.new_wait = False
            st.session_state.new_wait_for = ""
            st.experimental_rerun()

st.markdown("---")

# List ongoing tasks
st.markdown("## 🔍 Pågående oppgaver")
for task in st.session_state.tasks:
    with st.expander(task['title']):
        if task['wait']:
            st.info(f"⚠️ Venter på: {task['wait_for']}")
        progress = st.slider(
            "Fremdrift (%)",
            min_value=0,
            max_value=100,
            value=task['progress'],
            key=f"slider_{task['id']}",
            label_visibility="collapsed"
        )
        task['progress'] = progress
        if progress == 100:
            elapsed = (datetime.datetime.now() - task['created']).total_seconds() / 60
            task['time'] = elapsed
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
            st.experimental_rerun()
