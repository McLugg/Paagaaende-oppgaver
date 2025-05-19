import streamlit as st
import json
import os

st.set_page_config(page_title="Mine oppgaver", layout="centered")

DATA_FILE = "tasks.json"

# ─── Last inn tasks.json for persistens ───────────────────────────────────────
if "tasks" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.tasks = json.load(f)
    else:
        st.session_state.tasks = []

# ─── App-tittel og KPI ────────────────────────────────────────────────────────
st.title("✅ Mine oppgaver")
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"  # Placeholder for time-tracking
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", total)
col2.metric("Ferdig", done)
col3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# ─── Pågående oppgaver ──────────────────────────────────────────────────────
st.markdown("🔍 **Pågående oppgaver**")
to_remove = []

for idx, task in enumerate(st.session_state.tasks):
    percent = task["progress"]
    emoji = " 🙉" if task.get("wait_for") else ""
    header = f"{task['title']} — {percent}%{emoji}"

    with st.expander(header):
        st.write(task["desc"])
        if task.get("wait_for"):
            st.warning(f"Venter på: {task['wait_for']}")

        # Slider for fremdrift
        new_progress = st.slider(
            "Fremdrift (%)",
            min_value=0,
            max_value=100,
            value=percent,
            key=f"progress_{idx}",
        )

        # Hvis vi endret %, lagre og dump JSON umiddelbart
        if new_progress != percent:
            task["progress"] = new_progress
            with open(DATA_FILE, "w") as f:
                json.dump(st.session_state.tasks, f)

        # Custom arcade-style progress bar
        st.markdown(
            f"""
            <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
              <div style="
                background:#5FAA58;
                width:{task['progress']}%;
                height:100%;
                transform:skew(-10deg);
                box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;
              "></div>
              <div style="
                position:absolute;top:0;left:0;width:100%;
                text-align:center;line-height:24px;
                font-family:'Press Start 2P',monospace;
                color:#FFF;font-size:12px;
              ">{task['progress']}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Merk som fullført og fjern
        if task["progress"] == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
            to_remove.append(task)

# Fjern fullførte oppgaver etter at alle expanderne er bygget
if to_remove:
    for task in to_remove:
        st.session_state.tasks.remove(task)
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.tasks, f)

st.markdown("---")

# ─── Legg til ny oppgave ─────────────────────────────────────────────────────
with st.expander("➕ Legg til ny oppgave", expanded=True):
    with st.form("new_task_form", clear_on_submit=True):
        title = st.text_input("Tittel")
        desc = st.text_area("Beskrivelse")
        wait_for = st.text_input("Kommentar: Hva venter du på?")
        submit = st.form_submit_button("Legg til oppgave")

        if submit:
            if not title:
                st.error("❌ Tittel kan ikke være tom.")
            elif len(st.session_state.tasks) >= 10:
                st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
            else:
                new_task = {
                    "title": title,
                    "desc": desc,
                    "wait_for": wait_for.strip(),
                    "progress": 0,
                }
                st.session_state.tasks.append(new_task)
                # Lagre straks
                with open(DATA_FILE, "w") as f:
                    json.dump(st.session_state.tasks, f)
                st.success("🚀 Ny oppgave registrert!")
