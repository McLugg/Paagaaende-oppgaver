import streamlit as st
import json
import os
import random

# --- Konstanter ---
DATA_FILE = "tasks.json"
MOTIVATION = {
    25: [
        "💥 God start! Du er ¼ på vei!",
        "🚀 25 % allerede – imponerende!"
    ],
    50: [
        "🏆 Halveis! Stå på videre!",
        "⭐ 50 % – du ruller det inn!"
    ],
    75: [
        "🔥 75 % – nå er du nesten i mål!",
        "💪 ¾ gjort – fullfør det!"
    ],
    100: [
        "🎉 WOW – du fullførte oppgaven!",
        "🥳 Fantastisk jobb – oppgave slaktet!"
    ],
}

st.set_page_config(page_title="Mine oppgaver", layout="centered")

# --- Last inn tasks fra fil ---
if "tasks" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.tasks = json.load(f)
    else:
        st.session_state.tasks = []

# --- Hjelpefunksjon for å skrive til disk ---
def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.tasks, f, ensure_ascii=False, indent=2)

# --- Callback for slider-endring ---
def on_slider_change(idx):
    new_val = st.session_state[f"progress_{idx}"]
    st.session_state.tasks[idx]["progress"] = new_val
    save_tasks()
    # Gi motivasjonsmelding én gang per treff på terskel
    if new_val in MOTIVATION:
        msg = random.choice(MOTIVATION[new_val])
        st.success(msg)
        if new_val == 100:
            st.balloons()

# --- Header og KPI ---
st.title("✅ Mine oppgaver")
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["progress"] == 100)
avg_time = "-"  # Placeholder for fremtidig tidssporing
c1, c2, c3 = st.columns(3)
c1.metric("Oppgaver totalt", total)
c2.metric("Ferdig", done)
c3.metric("Snitt tid", f"{avg_time} min")
st.markdown("---")

# --- Pågående oppgaver først ---
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

        # Slider med on_change callback
        st.slider(
            "Fremdrift (%)",
            min_value=0, max_value=100,
            value=percent,
            key=f"progress_{idx}",
            on_change=on_slider_change,
            args=(idx,)
        )

        # Arcade‐bar i grønn
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

        if percent == 100:
            # Merk for sletting
            to_remove.append(idx)

# Fjern ferdige oppgaver umiddelbart
for idx in sorted(to_remove, reverse=True):
    st.session_state.tasks.pop(idx)
    save_tasks()

st.markdown("---")

# --- Formular for ny oppgave ---
with st.expander("➕ Legg til ny oppgave", expanded=True):
    with st.form("new_task_form", clear_on_submit=True):
        title    = st.text_input("Tittel")
        desc     = st.text_area("Beskrivelse")
        wait_for = st.text_input("Kommentar: Hva venter du på?")
        submit   = st.form_submit_button("Legg til oppgave")

        if submit:
            if not title:
                st.error("❌ Tittel kan ikke være tom.")
            elif len(st.session_state.tasks) >= 10:
                st.error("❌ Maks 10 oppgaver tillatt, fullfør noen først.")
            else:
                st.session_state.tasks.append({
                    "title":    title,
                    "desc":     desc,
                    "wait_for": wait_for.strip(),
                    "progress": 0
                })
                save_tasks()
                st.success("🚀 Ny oppgave registrert!")

