import streamlit as st

st.set_page_config(page_title="Mine oppgaver", layout="centered")

# Initialize session state for task list
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

# Add new task form with clear_on_submit to avoid manual session-state resets
with st.expander("➕ Legg til ny oppgave", expanded=True):
    with st.form("new_task_form", clear_on_submit=True):
        title = st.text_input("Tittel")
        desc = st.text_area("Beskrivelse")
        wait = st.checkbox("Venter på noen?")
        wait_for = ""
        if wait:
            wait_for = st.text_input("Kommentar: Hva venter du på?")
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
    # prepend egg emoji if there's a wait_for comment
    header = f"{'🥚 ' if task['wait_for'] else ''}{task['title']}"
    with st.expander(header):
        st.write(task["desc"])
        if task["wait"]:
            st.warning(f"Venter på: {task['wait_for']}")
        # Slider for progress
        progress = st.slider(
            "Fremdrift (%)", min_value=0, max_value=100,
            value=task["progress"], key=f"progress_{idx}"
        )
        task["progress"] = progress
        # Custom arcade‐inspirert progress bar i grønn #5FAA58
        percent = progress
        st.markdown(f"""
            <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
              <div style="
                background:#5FAA58;
                width:{percent}%;
                height:100%;
                transform:skew(-10deg);
                box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;
              "></div>
              <div style="
                position:absolute;top:0;left:0;width:100%;
                text-align:center;line-height:24px;
                font-family:'Press Start 2P',monospace;
                color:#FFF;font-size:12px;
              ">{percent}%</div>
            </div>
        """, unsafe_allow_html=True)
        if progress == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
