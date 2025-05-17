
import streamlit as st
import json
import os
import uuid
from datetime import datetime

DATA_FILE = 'tasks.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'tasks': [], 'completed': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize session state for form fields
for key in ['new_title', 'new_desc', 'new_wait', 'new_comment']:
    if key not in st.session_state:
        st.session_state[key] = '' if key != 'new_wait' else False

data = load_data()

st.set_page_config(page_title="Mine oppgaver", layout="centered")
st.title("✅ Mine oppgaver")

# Add new task
st.header("➕ Legg til ny oppgave")
with st.form('new_task'):
    title = st.text_input("Tittel", key='new_title')
    desc = st.text_area("Beskrivelse", key='new_desc')
    wait = st.checkbox("Venter på noen?", key='new_wait')
    comment = ''
    if wait:
        comment = st.text_input("Kommentar: Hva venter du på?", key='new_comment', max_chars=50)
    submitted = st.form_submit_button("Legg til")
    if submitted:
        if not title.strip():
            st.error("❌ Tittel kan ikke være tom.")
        elif len(data['tasks']) >= 10:
            st.error("❌ Maks 10 oppgaver nådd. Fullfør noen først.")
        else:
            task = {
                'id': str(uuid.uuid4()),
                'title': title.strip(),
                'description': desc.strip(),
                'wait': wait,
                'comment': comment.strip(),
                'progress': 0,
                'created': datetime.now().isoformat(),
                'completed': ''
            }
            data['tasks'].append(task)
            save_data(data)
            # clear form fields
            st.session_state['new_title'] = ''
            st.session_state['new_desc'] = ''
            st.session_state['new_wait'] = False
            st.session_state['new_comment'] = ''
            st.success("✅ Oppgave lagt til!")

st.markdown("---")
# Display ongoing tasks
st.header("🔍 Pågående oppgaver")
for idx, task in enumerate(data['tasks']):
    with st.expander(task['title']):
        st.write(task['description'])
        if task['wait'] and task['comment']:
            st.info(f"⚠️ Venter på: {task['comment']}")
        progress = st.slider("Fremdrift (%)", 0, 100, task['progress'], key=f"progress_{task['id']}")
        if progress != task['progress']:
            data['tasks'][idx]['progress'] = progress
            if progress == 100:
                data['tasks'][idx]['completed'] = datetime.now().isoformat()
                data['completed'].append(data['tasks'][idx])
                data['tasks'].pop(idx)
                st.success("🎉 Oppgave fullført!")
            save_data(data)

# Display completed tasks
if data['completed']:
    st.markdown("---")
    st.header("✅ Fullførte oppgaver")
    for t in data['completed']:
        st.write(f"- {t['title']} (Fullført: {t['completed'][:19]})")
