import streamlit as st
import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)

# --- INIT ---
st.set_page_config(page_title="Mine oppgaver", layout="centered")
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# --- HEADER + KPI ---
st.title("✅ Mine oppgaver")
total = len(st.session_state.tasks)
done  = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"
c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total)
c2.metric("Ferdig", done)
c3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# --- PÅGÅENDE OPPGAVER ---
st.markdown("🔍 **Pågående oppgaver**")
to_remove = []
for idx, task in enumerate(st.session_state.tasks):
    percent = task["progress"]
    emoji   = " 🙉" if task.get("wait_for") else ""
    header  = f"{task['title']} — {percent}%{emoji}"
    with st.expander(header):
        st.write(task["desc"])
        if task.get("wait_for"):
            st.warning(f"Venter på: {task['wait_for']}")
        new_p = st.slider(
            "Fremdrift (%)", 0, 100,
            value=percent, key=f"slider_{idx}"
        )
        if new_p != percent:
            task["progress"] = new_p
            save_tasks(st.session_state.tasks)
        # Arcade-bar
        st.markdown(f"""
            <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
              <div style="background:#5FAA58;width:{task['progress']}%;height:100%;transform:skew(-10deg);
                          box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;"></div>
              <div style="position:absolute;top:0;left:0;width:100%;text-align:center;
                          line-height:24px;font-family:'Press Start 2P',monospace;color:#FFF;
                          font-size:12px;">{task['progress']}%</div>
            </div>
        """, unsafe_allow_html=True)
        if task["progress"] == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
            to_remove.append(idx)

# Fjern fullførte oppgaver (fra høyeste indeks først)
for i in sorted(to_remove, reverse=True):
    st.session_state.tasks.pop(i)
    save_tasks(st.session_state.tasks)

st.markdown("---")

# --- LEGG TIL OPPGAVE ---
with st.expander("➕ Legg til ny oppgave", expanded=True):
    new_title    = st.text_input("Tittel", key="ti")
    new_desc     = st.text_area("Beskrivelse", key="de")
    new_wait_for = st.text_input("Kommentar: Hva venter du på?", key="wf")
    if st.button("Legg til oppgave", key="add"):
        if not new_title.strip():
            st.error("❌ Tittel kan ikke være tom.")
        elif len(st.session_state.tasks) >= 10:
            st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
        else:
            st.session_state.tasks.append({
                "title":    new_title.strip(),
                "desc":     new_desc.strip(),
                "wait_for": new_wait_for.strip(),
                "progress": 0
            })
            save_tasks(st.session_state.tasks)
            st.success("🚀 Ny oppgave registrert!")
            # Clear inputs
            st.session_state["ti"] = ""
            st.session_state["de"] = ""
            st.session_state["wf"] = ""
