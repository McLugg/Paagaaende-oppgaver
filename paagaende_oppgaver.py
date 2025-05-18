import streamlit as st

st.set_page_config(page_title="Mine oppgaver", layout="centered")

# Persistent storage for tasks across page refresh
@st.experimental_singleton
def get_task_list():
    return []

tasks = get_task_list()

# Title and KPIs
st.title("✅ Mine oppgaver")
total = len(tasks)
done = sum(1 for t in tasks if t.get("progress") == 100)
avg_time = "-"
c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total)
c2.metric("Ferdig", done)
c3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# Add new task form
def add_task():
    title = st.session_state.title
    desc = st.session_state.desc
    wait = st.session_state.wait
    wait_for = st.session_state.wait_for.strip()

    if not title:
        st.error("❌ Tittel kan ikke være tom.")
        return
    if len(tasks) >= 10:
        st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
        return

    new = {"title": title, "desc": desc, "progress": 0}
    if wait and wait_for:
        new["wait_for"] = wait_for

    tasks.append(new)
    st.success("🚀 Ny oppgave registrert!")
    # Clear form inputs
    st.session_state.title = ""
    st.session_state.desc = ""
    st.session_state.wait = False
    st.session_state.wait_for = ""

with st.form("new_task_form", clear_on_submit=True):
    st.markdown("### ➕ Legg til ny oppgave")
    st.text_input("Tittel", key="title")
    st.text_area("Beskrivelse", key="desc")
    st.checkbox("Venter på noen?", key="wait")
    st.text_input("Kommentar: Hva venter du på?", key="wait_for")
    st.form_submit_button("Legg til oppgave", on_click=add_task)

st.markdown("---")
st.markdown("## 🔍 Pågående oppgaver")

# Display tasks
for i, task in enumerate(tasks):
    percent = task.get("progress", 0)
    emoji = " 🙉" if task.get("wait_for") else ""
    header = f"{task['title']} — {percent}%{emoji}"
    with st.expander(header):
        st.write(task["desc"])
        if task.get("wait_for"):
            st.warning(f"Venter på: {task['wait_for']}")

        p = st.slider("Fremdrift (%)", 0, 100, percent, key=f"prog_{i}")
        task["progress"] = p

        # 90-talls arcade-stil grønn progressbar
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
                color:#FFF;font-size:12px;">
                {p}%
              </div>
            </div>
        """, unsafe_allow_html=True)

        if p == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
