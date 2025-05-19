import streamlit as st
import json
import os

DATA_FILE = "tasks.json"
st.set_page_config(page_title="Mine oppgaver", layout="centered")

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)

# ─── Init ──────────────────────────────────────────────────────────
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# ─── Tittel + KPI ─────────────────────────────────────────────────
st.title("✅ Mine oppgaver")
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"  # Placeholder
c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total)
c2.metric("Ferdig", done)
c3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# ─── Reservér en plassering for listen over oppgaver ─────────────
tasks_placeholder = st.container()

# ─── Skjema for ny oppgave ─────────────────────────────────────────
with st.expander("➕ Legg til ny oppgave", expanded=True):
    with st.form("new_task_form", clear_on_submit=True):
        title     = st.text_input("Tittel")
        desc      = st.text_area("Beskrivelse")
        wait_for  = st.text_input("Kommentar: Hva venter du på?")
        submitted = st.form_submit_button("Legg til oppgave")

        if submitted:
            if not title:
                st.error("❌ Tittel kan ikke være tom.")
            elif len(st.session_state.tasks) >= 10:
                st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
            else:
                st.session_state.tasks.append({
                    "title":     title,
                    "desc":      desc,
                    "wait_for":  wait_for.strip(),
                    "progress":  0,
                })
                save_tasks(st.session_state.tasks)
                st.success("🚀 Ny oppgave registrert!")

# ─── Tegn listen over oppgaver (umiddelbart etter skjemaet, men placeholder gjør at det ligger øverst) ─────
with tasks_placeholder:
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
                "Fremdrift (%)",
                0, 100,
                value=percent,
                key=f"progress_{idx}",
            )
            if new_p != percent:
                st.session_state.tasks[idx]["progress"] = new_p
                save_tasks(st.session_state.tasks)

            # Arcade‐bar
            st.markdown(f"""
                <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
                  <div style="
                    background:#5FAA58;
                    width:{new_p}%;
                    height:100%;
                    transform:skew(-10deg);
                    box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;
                  "></div>
                  <div style="
                    position:absolute;top:0;left:0;width:100%;
                    text-align:center;line-height:24px;
                    font-family:'Press Start 2P',monospace;
                    color:#FFF;font-size:12px;
                  ">{new_p}%</div>
                </div>
            """, unsafe_allow_html=True)

            if new_p == 100:
                st.success("🎉 Fantastisk! Oppgaven er fullført!")
                to_remove.append(idx)

    # Fjern 100%-oppgaver
    for i in sorted(to_remove, reverse=True):
        st.session_state.tasks.pop(i)
    if to_remove:
        save_tasks(st.session_state.tasks)
