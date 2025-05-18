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
        "wait_for": st.session_state.wait_for,
        "progress": 0
    })
    st.success("🚀 Ny oppgave registrert!")
    # Reset inputs
    st.session_state.title = ""
    st.session_state.desc = ""
    st.session_state.wait = False
    st.session_state.wait_for = ""

def show_insp():
    # Eksempel på AI-generert inspirerende melding
    insp_msgs = [
        "💪 Du er på god vei!",
        "🚀 Fortsett slik!",
        "🔥 Keep the fire burning!",
        "🎮 Du er en boss!"
    ]
    st.toast(insp_msgs[st.session_state.tasks[-1]["progress"] // 25 % len(insp_msgs)])

# Title
st.title("✅ Mine oppgaver")

# Status metrics
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"  # Placeholder, tidssporing ikke implementert
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", total)
col2.metric("Ferdig", done)
col3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# Pågående oppgaver
st.markdown("🔍 **Pågående oppgaver**")
for i, task in enumerate(st.session_state.tasks):
    # Header: tittel — % ferdig + emoji om vent
    pct = task["progress"]
    emo = " 🙉" if task["wait_for"] else ""
    header = f"{task['title']} — {pct}%{emo}"
    with st.expander(header):
        st.write(task["desc"])
        if task["wait_for"]:
            st.warning(f"Venter på: {task['wait_for']}")
        p = st.slider(
            "Fremdrift (%)", min_value=0, max_value=100,
            value=task["progress"], key=f"prog_{i}"
        )
        task["progress"] = p
        # Arcade-inspirert grønn bar
        st.markdown(f"""
            <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
              <div style="
                background:#5FAA58;
                width:{p}%;
                height:100%;
                transform:skew(-10deg);
                box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;
              "></div>
              <div style="
                position:absolute;top:0;left:0;width:100%;
                text-align:center;line-height:24px;
                font-family:'Press Start 2P',monospace;
                color:#FFF;font-size:12px;
              ">{p}%</div>
            </div>
        """, unsafe_allow_html=True)
        if p == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
            show_insp()

st.markdown("---")
# Legg til ny oppgave
st.text_input("Tittel", key="title")
st.text_area("Beskrivelse", key="desc")
st.checkbox("Venter på noen?", key="wait")
if st.session_state.wait:
    st.text_input("Kommentar: Hva venter du på?", key="wait_for")

if st.button("Legg til oppgave", on_click=add_task, key="add_btn"):
    pass
