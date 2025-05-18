import streamlit as st

st.set_page_config(page_title="Mine oppgaver", layout="centered")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Title and status metrics
st.title("✅ Mine oppgaver")
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", total)
col2.metric("Ferdig", done)
col3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# Form for adding a new task
with st.form("new_task_form", clear_on_submit=True):
    st.text_input("Tittel", key="new_title")
    st.text_area("Beskrivelse", key="new_desc")
    st.checkbox("Venter på noen?", key="new_wait")
    if st.session_state.new_wait:
        st.text_input("Kommentar: Hva venter du på?", key="new_wait_for")
    submitted = st.form_submit_button("Legg til oppgave")
    if submitted:
        if not st.session_state.new_title:
            st.error("❌ Tittel kan ikke være tom.")
        elif total >= 10:
            st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
        else:
            st.session_state.tasks.append({
                "title": st.session_state.new_title,
                "desc": st.session_state.new_desc,
                "wait": st.session_state.new_wait,
                "wait_for": st.session_state.new_wait_for,
                "progress": 0
            })
            st.success("🚀 Ny oppgave registrert!")

st.markdown("---")
st.markdown("🔍 **Pågående oppgaver**")

# Display tasks
for idx, task in enumerate(st.session_state.tasks):
    with st.expander(task["title"]):
        st.write(task["desc"])
        if task["wait"]:
            st.warning(f"⚠️ Venter på: {task['wait_for']}")
        progress = st.slider("Fremdrift (%)", 0, 100, task["progress"], key=f"progress_{idx}")
        task["progress"] = progress
        bar = f"""<div style='background:#ddd;border-radius:8px;overflow:hidden;'>
  <div style='background:#5FAA58;width:{progress}%;padding:8px;color:#fff;font-weight:bold;text-align:center;font-family:monospace;'>
    {progress}%</div>
</div>"""
        st.markdown(bar, unsafe_allow_html=True)
        if progress == 100:
            st.success("🌟 Fantastisk! Du har fullført oppgaven!")
