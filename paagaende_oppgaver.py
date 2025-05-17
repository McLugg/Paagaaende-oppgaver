import streamlit as st

st.set_page_config(page_title="Mine oppgaver", layout="centered")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Title
st.title("✅ Mine oppgaver")

# Status metrics
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"  # Placeholder, time tracking not implemented
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", total)
col2.metric("Ferdig", done)
col3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# Add new task form using st.form to manage input state reset
with st.expander("➕ Legg til ny oppgave", expanded=True):
    with st.form("new_task_form", clear_on_submit=True):
        title = st.text_input("Tittel")
        desc = st.text_area("Beskrivelse")
        wait = st.checkbox("Venter på noen?")
        wait_for = ""
        if wait:
            wait_for = st.text_input("Hva venter du på?")
        submit = st.form_submit_button("Legg til oppgave")

        if submit:
            if not title:
                st.error("❌ Tittel kan ikke være tom.")
            elif total >= 10:
                st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
            else:
                st.session_state.tasks.append({
                    "title": title,
                    "desc": desc,
                    "wait": wait,
                    "wait_for": wait_for,
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
            st.warning(f"Venter på: {task['wait_for']}")
        # Slider for progress
        progress = st.slider(
            "Fremdrift (%)", min_value=0, max_value=100,
            value=task["progress"], key=f"progress_{idx}"
        )
        task["progress"] = progress
        # Custom green bar color via HTML/CSS trick
        percent = task["progress"]
        st.markdown(f"""
            <div style=\"background-color: #e0e0e0; border-radius: 8px; overflow: hidden; width: 100%;\">
                <div style=\"width: {percent}%; background-color: #5FAA58; color: white; padding: 4px 0; text-align: center; font-weight: bold; border-radius: 8px;\">
                    {percent}% Fullført
                </div>
            </div>
        """, unsafe_allow_html=True)
        if progress == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")

