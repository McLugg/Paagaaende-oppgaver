
import streamlit as st
import json
import os
import uuid
from datetime import datetime

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'tasks': [], 'completed': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# App setup
st.set_page_config(page_title="Mine oppgaver", layout="centered")
st.title("✅ Mine oppgaver")

data = load_data()

# Add new task
st.subheader("➕ Legg til ny oppgave")
with st.form("new_task"):
    title = st.text_input("Tittel", key="new_title")
    desc = st.text_area("Beskrivelse", key="new_desc")
    wait = st.checkbox("Venter på noen?", key="new_wait")
    comment = ""
    if wait:
        comment = st.text_input("Kommentar: Hva venter du på?", key="new_comment")
    submitted = st.form_submit_button("Legg til")
    if submitted:
        if not title.strip():
            st.error("❌ Tittel kan ikke være tom.")
        elif len(data['tasks']) >= 10:
            st.error("❌ Maks 10 oppgaver. Fullfør noen først.")
        else:
            now = datetime.now().isoformat()
            task = {
                'id': str(uuid.uuid4()),
                'title': title,
                'description': desc,
                'wait': wait,
                'comment': comment,
                'progress': 0,
                'created_at': now,
                'completed_at': ''
            }
            data['tasks'].append(task)
            save_data(data)
            st.success("✅ Oppgave lagt til!")
            # Reset form fields
            st.session_state.new_title = ''
            st.session_state.new_desc = ''
            st.session_state.new_wait = False
            st.session_state.new_comment = ''

# Display ongoing tasks
st.markdown('---')
st.subheader("🔍 Pågående oppgaver")
for idx, t in enumerate(data['tasks']):
    key = f"progress_{t['id']}"
    cols = st.columns([4,1])
    with cols[0]:
        st.markdown(f"**{t['title']}**")
        st.write(t['description'])
        if t['wait'] and t['comment']:
            st.info(f"⚠️ Venter på: {t['comment']}")
    with cols[1]:
        progress = st.slider("", 0, 100, t['progress'], key=key)
        if progress != t['progress']:
            t['progress'] = progress
            if progress == 100:
                t['completed_at'] = datetime.now().isoformat()
                data['completed'].append(t)
                data['tasks'].pop(idx)
                st.success("🎉 Oppgave fullført!")
            save_data(data)

# Display completed tasks
if data['completed']:
    st.markdown('---')
    st.subheader("✅ Fullførte oppgaver")
    for t in data['completed']:
        st.write(f"- {t['title']} (Fullført: {t.get('completed_at', '-')})")
