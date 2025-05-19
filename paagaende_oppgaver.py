import streamlit as st
import json
import os
import random
import uuid

# --- Konstanter og filstier ---
DATA_FILE = "tasks.json"
STATS_FILE = "stats.json"

# --- Sideoppsett ---
st.set_page_config(page_title="Mine oppgaver", layout="centered")

# --- Last inn tasks ---
if "tasks" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            st.session_state.tasks = json.load(f)
    else:
        st.session_state.tasks = []
    # Migrer tasks uten id
    updated = False
    for task in st.session_state.tasks:
        if "id" not in task:
            task["id"] = str(uuid.uuid4())
            updated = True
    if updated:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.tasks, f, ensure_ascii=False, indent=2)

# --- Last inn statistikk ---
if "completed_count" not in st.session_state:
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            st.session_state.completed_count = data.get("completed", 0)
    else:
        st.session_state.completed_count = 0

# --- Surprise defaults ---
default_gif = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmRuMWJxdmhzaHU4Z2Myd3g5bXZsaWRnMDJ6eHNjZnZyNmt3d3NhdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tPplGWjN0xLybiU/giphy.gif"
default_image = "https://imgflip.com/i/9uj9l8"
default_css = """
<style>
@keyframes glow { 0% { text-shadow: 0 0 5px #5FAA58; } 50% { text-shadow: 0 0 20px #80c372; } 100% { text-shadow: 0 0 5px #5FAA58; }}
.glow-banner { font-family: 'Press Start 2P', monospace; font-size: 24px; color: #5FAA58; animation: glow 1.5s infinite; text-align: center; margin: 16px 0; }
</style>
<div class="glow-banner"> 🕹 LEVEL UP! YOU DID IT! 🕹 </div>
"""

# Initialize surprise settings
if "surprise_mode" not in st.session_state:
    st.session_state.surprise_mode = "GIF"
if "surprise_gif" not in st.session_state:
    st.session_state.surprise_gif = default_gif
if "surprise_image" not in st.session_state:
    st.session_state.surprise_image = default_image
if "surprise_css" not in st.session_state:
    st.session_state.surprise_css = default_css

# --- Hjelpefunksjoner ---
def save_tasks():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.tasks, f, ensure_ascii=False, indent=2)

def save_stats():
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump({"completed": st.session_state.completed_count}, f)

def get_surprise_html():
    mode = st.session_state.surprise_mode
    if mode == "GIF":
        return f"""
<div style="text-align:center; margin:16px 0;">
  <img src="{st.session_state.surprise_gif}" alt="Surprise GIF" width="200" />
</div>
"""
    elif mode == "Image":
        return f"""
<div style="text-align:center; margin:16px 0;">
  <img src="{st.session_state.surprise_image}" alt="Surprise Img" width="200" />
</div>
"""
    else:
        return st.session_state.surprise_css

MOTIVATION = {
    25: ["💥 God start! Du er ¼ på vei!", "🚀 25% allerede – imponert!"],
    50: ["🏆 Halveis! Stå på videre!", "⭐ 50% – du ruller det inn!"],
    75: ["🔥 75% – nå er du nesten i mål!", "💪 ¾ gjort – fullfør det!"],
   100: ["🎉 WOW – du fullførte oppgaven!", "🥳 Fantastisk jobb – oppgave slaktet!"],
}

def on_slider_change(task_id: str):
    task = next((t for t in st.session_state.tasks if t.get("id") == task_id), None)
    if not task:
        return
    new_val = st.session_state[f"progress_{task_id}"]
    if new_val != task["progress"]:
        task["progress"] = new_val
        save_tasks()
        if new_val in MOTIVATION:
            st.success(random.choice(MOTIVATION[new_val]))
        if new_val == 100:
            st.session_state.completed_count += 1
            save_stats()
            st.balloons()
            st.markdown(get_surprise_html(), unsafe_allow_html=True)
            if st.session_state.completed_count % 5 == 0:
                st.success(f"✨ Du har fullført {st.session_state.completed_count} oppgaver! ✨")
                st.markdown(
                    f"""
<marquee behavior="smooth" direction="left" scrollamount="15">
  <span style="font-size:48px;">🚀</span>
</marquee>
""", unsafe_allow_html=True)

# --- Header og KPI ---
st.title("✅ Mine oppgaver")
total = len(st.session_state.tasks)
done  = st.session_state.completed_count
c1, c2 = st.columns(2)
c1.metric("Oppgaver totalt", total)
c2.metric("Oppgaver fullført", done)
st.markdown("---")

# --- Legg til ny oppgave (øverst) ---
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
                st.error("❌ Maks 10 oppgaver tillatt.")
            else:
                new_task = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "desc": desc,
                    "wait_for": wait_for.strip(),
                    "progress": 0
                }
                st.session_state.tasks.append(new_task)
                save_tasks()
                st.success("🚀 Ny oppgave registrert!")

st.markdown("---")

# --- Pågående oppgaver ---
st.markdown("🔍 **Pågående oppgaver**")
to_remove = []
for task in st.session_state.tasks:
    percent = task.get("progress", 0)
    emoji   = " 🙉" if task.get("wait_for") else ""
    header  = f"{task['title']} — {percent}%{emoji}"
    tid     = task["id"]
    with st.expander(header, expanded=True):
        st.write(task.get("desc", ""))
        if task.get("wait_for"):
            st.warning(f"Venter på: {task['wait_for']}")
        st.slider(
            "Fremdrift (%)", min_value=0, max_value=100,
            value=percent, key=f"progress_{tid}",
            on_change=on_slider_change, args=(tid,)
        )
        st.markdown(f"""
            <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
              <div style="background:#5FAA58;width:{percent}%;height:100%;transform:skew(-10deg);box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;"></div>
              <div style="position:absolute;top:0;left:0;width:100%;text-align:center;line-height:24px;font-family:'Press Start 2P',monospace;color:#FFF;font-size:12px;">{percent}%</div>
            </div>
        """, unsafe_allow_html=True)
        if percent == 100:
            to_remove.append(task["id"])

for tid in to_remove:
    st.session_state.tasks = [t for t in st.session_state.tasks if t.get("id") != tid]
save_tasks()

# --- Innstillinger ---
st.markdown("---")
st.subheader("⚙️ Innstillinger overraskelse")
mode = st.radio("Velg overraskelse som vises ved fullføring:", ["GIF", "Image", "CSS"],
                index=["GIF","Image","CSS"].index(st.session_state.surprise_mode))
st.session_state.surprise_mode = mode
colg, coli, colc = st.columns(3)
with colg:
    gif_url = st.text_input("GIF URL", st.session_state.surprise_gif)
    st.session_state.surprise_gif = gif_url
with coli:
    img_url = st.text_input("Image URL", st.session_state.surprise_image)
    st.session_state.surprise_image = img_url
with colc:
    css_in = st.text_area("CSS Banner HTML/CSS", st.session_state.surprise_css, height=150)
    st.session_state.surprise_css = css_in
