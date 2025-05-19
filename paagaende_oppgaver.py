import streamlit as st
import json
import os

# ─── Konfigurasjon ────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mine oppgaver", layout="centered")
DATA_FILE = "tasks.json"

# ─── Hjelpe‐funksjoner for lagring ───────────────────────────────────────────
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)

# ─── Initialiser session_state.tasks ────────────────────────────────────────
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# ─── Tittel og KPI ────────────────────────────────────────────────────────────
st.title("✅ Mine oppgaver")
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"  # Vi kan legge til tidssporing senere
col1, col2, col3 = st.columns(3)
col1.metric("Oppgaver totalt", total)
col2.metric("Ferdig", done)
col3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# ─── Pågående oppgaver (øverst) ───────────────────────────────────────────────
st.markdown("🔍 **Pågående oppgaver**")

# Vi samler dem vi må fjerne (100% fullført)
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

        # Hvis endret, oppdater og lagre
        if new_progress != percent:
            st.session_state.tasks[idx]["progress"] = new_progress
            save_tasks(st.session_state.tasks)

        # Arcade‐stil progress bar
        st.markdown(
            f"""
            <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
              <div style="
                background:#5FAA58;
                width:{new_progress}%;
                height:100%;
                transform:skew(-10deg);
                box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;
              "></div>
              <div style="
                position:absolute;top:0;left:0;width:100%;
                text-align:center;line-height:24px;
                font-family:'Press Start 2P',monospace;
                color:#FFF;font-size:12px;
              ">{new_progress}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Merk for fjerning hvis fullført
        if new_progress == 100:
            st.success("🎉 Fantastisk! Oppgaven er fullført!")
            to_remove.append(idx)

# Fjern completed tasks bakerst for å unngå index‐skjevheter
for i in sorted(to_remove, reverse=True):
    st.session_state.tasks.pop(i)
save_tasks(st.session_state.tasks)

st.markdown("---")

# ─── Legg til ny oppgave (nederst) ───────────────────────────────────────────
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
                # Append og lagre umiddelbart
                st.session_state.tasks.append({
                    "title": title,
                    "desc": desc,
                    "wait_for": wait_for.strip(),
                    "progress": 0,
                })
                save_tasks(st.session_state.tasks)
                st.success("🚀 Ny oppgave registrert!")
