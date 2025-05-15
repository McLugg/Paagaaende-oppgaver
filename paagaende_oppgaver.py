
import streamlit as st
import json
import os
from datetime import datetime

DATA_PATH = 'data.json'

# Load or initialize data
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
else:
    data = {'tasks': [], 'completed': []}

st.set_page_config(page_title='Mine oppgaver')

# --- Status KPI ---
total = len(data['tasks']) + len(data['completed'])
done = len(data['completed'])
avg_time = round(
    sum((datetime.fromisoformat(t['completed_at']) - datetime.fromisoformat(t['created_at'])).total_seconds()
        for t in data['completed']) / done / 60, 1
) if done else '-'

col1, col2, col3 = st.columns(3)
col1.metric('Oppgaver totalt', total)
col2.metric('Ferdig', done)
col3.metric('Snitt tid', f'{avg_time} min' if done != '-' else '-')

st.markdown('---')

# --- Add new task ---
st.header('➕ Legg til ny oppgave')
with st.form('new_task_form', clear_on_submit=True):
    title = st.text_input('Tittel')
    desc = st.text_area('Beskrivelse')
    wait_flag = st.checkbox('Venter på noen?')
    wait_note = ''
    if wait_flag:
        wait_note = st.text_input('Hva venter du på?')
    submitted = st.form_submit_button('Legg til oppgave')
    if submitted:
        if not title:
            st.error('Oppgave må ha en tittel.')
        elif len(data['tasks']) >= 10:
            st.warning('🎉 Du har nådd maks antall oppgaver! Fullfør noen først.')
        else:
            task = {
                'id': int(datetime.now().timestamp()*1000),
                'title': title,
                'desc': desc,
                'wait_flag': wait_flag,
                'wait_note': wait_note,
                'status': 0,
                'created_at': datetime.now().isoformat()
            }
            data['tasks'].append(task)
            with open(DATA_PATH, 'w') as f:
                json.dump(data, f)
            st.success('✅ Oppgave lagt til!')

st.markdown('---')

# --- Ongoing tasks ---
st.header('🔍 Pågående oppgaver')
for o in data['tasks']:
    with st.expander(o['title']):
        if o['wait_flag']:
            st.warning(f"Venter på: {o['wait_note']}")
        # slider for progress
        prog = st.slider(
            label='Fremdrift %',
            min_value=0,
            max_value=100,
            value=o['status'],
            key=f"slider_{o['id']}"
        )
        if prog != o['status']:
            o['status'] = prog
            if prog == 100:
                o['completed_at'] = datetime.now().isoformat()
                data['completed'].append(o)
                data['tasks'] = [t for t in data['tasks'] if t['id'] != o['id']]
                st.balloons()
                st.success('🎉 Oppgave fullført!')
            with open(DATA_PATH, 'w') as f:
                json.dump(data, f)
        st.markdown(f"**{o['status']}% fullført**")
