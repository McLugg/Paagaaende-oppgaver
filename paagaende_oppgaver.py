import streamlit as st
import json
import time
from datetime import datetime

DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'tasks': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def ai_message(event_type):
    if event_type == 'add_limit':
        return "😅 Du har nådd maks antall oppgaver! Løs noen først før du legger til nye."
    if event_type == 'complete':
        return "🎉 Fantastisk! Oppgaven er fullført!"

data = load_data()

st.title("✅ Mine oppgaver")

# KPI
total = len(data['tasks'])
done = len([t for t in data['tasks'] if t['progress'] >= 100])
times = [t.get('duration', 0) for t in data['tasks'] if 'duration' in t]
avg_time = f"{sum(times)/len(times):.1f} min" if times else '-'
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", total)
col2.metric("Ferdig", done)
col3.metric("Snitt tid", avg_time)

st.markdown("---")

# Add new task form
with st.expander("➕ Legg til ny oppgave", expanded=True):
    title = st.text_input("Tittel")
    desc = st.text_area("Beskrivelse")
    waiting = st.checkbox("Venter på noen?")
    wait_msg = ""
    if waiting:
        wait_msg = st.text_input("Hva venter du på?", max_chars=50, placeholder="Skriv hvem eller hva du venter på")
    if st.button("Legg til oppgave"):
        if total >= 10:
            st.warning(ai_message('add_limit'))
        elif title:
            new_task = {
                'id': int(time.time()*1000),
                'title': title,
                'desc': desc,
                'waiting': waiting,
                'wait_msg': wait_msg,
                'progress': 0,
                'created': datetime.now().isoformat()
            }
            data['tasks'].append(new_task)
            save_data(data)
            st.success("🚀 Ny oppgave registrert!")
            st.experimental_rerun()

st.markdown("---")

# Display ongoing tasks
st.subheader("🔍 Pågående oppgaver")
for t in data['tasks']:
    with st.expander(t['title']):
        if t['waiting'] and t['wait_msg']:
            st.info(f"⚠️ Venter på: {t['wait_msg']}")
        progress = st.slider("Fremdrift (%)", 0, 100, t['progress'], key=f"slider_{t['id']}")
        if progress != t['progress']:
            t['progress'] = progress
            if progress >= 100:
                t['completed_at'] = datetime.now().isoformat()
                t['duration'] = (datetime.fromisoformat(t['completed_at']) - datetime.fromisoformat(t['created'])).total_seconds() / 60
                st.success(ai_message('complete'))
            save_data(data)
            st.experimental_rerun()
        st.progress(progress, text=f"{progress}% fullført")
