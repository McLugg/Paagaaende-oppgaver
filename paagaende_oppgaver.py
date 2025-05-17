import streamlit as st

st.set_page_config(page_title="Mine oppgaver", layout="centered")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "new_title" not in st.session_state:
    st.session_state.new_title = ""
if "new_desc" not in st.session_state:
    st.session_state.new_desc = ""
if "new_wait" not in st.session_state:
    st.session_state.new_wait = False
if "new_comment" not in st.session_state:
    st.session_state.new_comment = ""

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

# Add new task form
with st.expander("➕ Legg til ny oppgave", expanded=True):
    st.text_input("Tittel", key="new_title")
    st.text_area("Beskrivelse", key="new_desc")
    st.checkbox("Venter på noen?", key="new_wait")
    # Only show comment field if waiting is checked
    if st.session_state.new_wait:
        st.text_input("Kommentar: Hva venter du på?", key="new_comment")
    if st.button("Legg til oppgave"):
        if not st.session_state.new_title:
            st.error("❌ Tittel kan ikke være tom.")
        elif total >= 10:
            st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
        else:
            st.session_state.tasks.append({
                "title": st.session_state.new_title,
                "desc": st.session_state.new_desc,
                "wait": st.session_state.new_wait,
                "wait_for": st.session_state.new_comment,
                "progress": 0
            })
            # Clear inputs
            st.session_state.new_title = ""
            st.session_state.new_desc = ""
            st.session_state.new_wait = False
            st.session_state.new_comment = ""
            st.success("🚀 Ny oppgave registrert!")

st.markdown("---")
st.markdown("🔍 **Pågående oppgaver**")

# Display tasks
for idx, task in enumerate(st.session_state.tasks):
    with st.expander(task["title"]):
        st.write(task["desc"])
        if task["wait"]:
            st.warning(f"Venter på: {task['wait_for']}")
        progress = st.slider(
            "Fremdrift (%)", min_value=0, max_value=100,
            value=task["progress"], key=f"progress_{idx}"
        )
        task["progress"] = progress
        st.progress(progress / 100.0)
        if progress == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
