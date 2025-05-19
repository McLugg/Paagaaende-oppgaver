
import streamlit as st
import json
import os
import random
import uuid

# --- Konstanter og filstier ---
DATA_FILE = "tasks.json"
STATS_FILE = "stats.json"
SETTINGS_FILE = "settings.json"

# Overraskelses-eksempler (kan endres i innstillinger)
DEFAULT_SURPRISE = {
    "type": "gif",  # options: 'gif', 'image', 'css'
    "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmRuMWJxdmhzaHU4Z2Myd3g5bXZsaWRnMDJ6eHNjZnZyNmt3d3NhdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tPplGWjN0xLybiU/giphy.gif",
    "image": "https://imgflip.com/i/9uj9l8",
    "css": "<style>@keyframes glow{0%{text-shadow:0 0 5px #5FAA58;}50%{text-shadow:0 0 20px #80c372;}100%{text-shadow:0 0 5px #5FAA58;}}.glow-banner{font-family:'Press Start 2P', monospace;font-size:24px;color:#5FAA58;animation:glow 1.5s infinite;text-align:center;margin:16px 0;}</style><div class='glow-banner'>🕹 LEVEL UP! YOU DID IT! 🕹</div>"
}

# Motivasjonsmeldinger ved 25%, 50%, 75% og 100%
MOTIVATION = {
    25: ["💥 God start! Du er ¼ på vei!", "🚀 25% allerede – imponer!"],
    50: ["🏆 Halveis! Stå på videre!", "⭐ 50% – du ruller det inn!"],
    75: ["🔥 75% – nesten i mål!", "💪 ¾ gjort – fullfør!"],
   100: ["🎉 WOW – oppgave fullført!", "🥳 Supert jobba!"],
}

# --- Hjelpefunksjoner ---
def save_tasks():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.tasks, f, ensure_ascii=False, indent=2)

def save_stats():
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump({"completed": st.session_state.completed_count}, f)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_SURPRISE.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

# Callback for slider-endring
def on_slider_change(task_id: str):
    task = next((t for t in st.session_state.tasks if t.get("id") == task_id), None)
    if not task:
        return
    new_val = st.session_state[f"progress_{task_id}"]
    if new_val != task["progress"]:
        task["progress"] = new_val
        save_tasks()
        # motivasjon
        if new_val in MOTIVATION:
            st.success(random.choice(MOTIVATION[new_val]))
        # fullført
        if new_val == 100:
            st.session_state.completed_count += 1
            save_stats()
            st.balloons()
            # vis overraskelse
            s = st.session_state.settings
            if s["type"] == "gif":
                st.image(s["gif"], width=200)
            elif s["type"] == "image":
                st.markdown(f"<img src='{s['image']}' width='200'>", unsafe_allow_html=True)
            else:
                st.markdown(s["css"], unsafe_allow_html=True)
            # ekstra feiring hver 5 fullført
            if st.session_state.completed_count % 5 == 0:
                st.success(f"✨ {st.session_state.completed_count} oppgaver fullført! ✨")
                st.markdown(
                    f"<marquee behavior='smooth' direction='left' scrollamount='15'><span style='font-size:48px;'>₿</span></marquee>",
                    unsafe_allow_html=True
                )

# --- Sideoppsett ---
st.set_page_config(page_title="Mine oppgaver", layout="centered")

# --- Last inn tasks ---
if "tasks" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            st.session_state.tasks = json.load(f)
    else:
        st.session_state.tasks = []
    # migrer uten id
    updated = False
    for t in st.session_state.tasks:
        if "id" not in t:
            t["id"] = str(uuid.uuid4())
            updated = True
    if updated:
        save_tasks()

# --- Last inn statistikk ---
if "completed_count" not in st.session_state:
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            st.session_state.completed_count = json.load(f).get("completed", 0)
    else:
        st.session_state.completed_count = 0

# --- Last inn innstillinger ---
if "settings" not in st.session_state:
    st.session_state.settings = load_settings()

# --- Header + KPI ---
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
                new_t = {"id": str(uuid.uuid4()), "title": title, "desc": desc,
                         "wait_for": wait_for.strip(), "progress": 0}
                st.session_state.tasks.append(new_t)
                save_tasks()
                st.experimental_rerun()

st.markdown("---")

# --- Pågående oppgaver ---
st.markdown("🔍 **Pågående oppgaver**")
to_remove = []
for task in st.session_state.tasks:
    pid = task.get("id")
    percent = task.get("progress",0)
    emoji   = " 🙉" if task.get("wait_for") else ""
    header  = f"{task['title']} — {percent}%{emoji}"
    with st.expander(header, expanded=False):
        st.write(task.get("desc",""))
        if task.get("wait_for"):
            st.warning(f"Venter på: {task['wait_for']}")
        st.slider("Fremdrift (%)", 0, 100, value=percent,
                  key=f"progress_{pid}", on_change=on_slider_change, args=(pid,))
        st.markdown(f"""
            <div style="background:#222;border:2px solid #5FAA58;border-radius:4px;height:24px;position:relative;">
              <div style="background:#5FAA58;width:{percent}%;height:100%;transform:skew(-10deg);box-shadow:0 0 8px #5FAA58,inset 0 0 4px #80c372;"></div>
              <div style="position:absolute;top:0;left:0;width:100%;text-align:center;line-height:24px;font-family:'Press Start 2P',monospace;color:#FFF;font-size:12px;">{percent}%</div>
            </div>
        """, unsafe_allow_html=True)
        if percent == 100:
            to_remove.append(pid)

# --- Fjern ferdige oppgaver ---
for pid in to_remove:
    st.session_state.tasks = [t for t in st.session_state.tasks if t.get("id")!=pid]
    save_tasks()

# --- Innstillinger (collapsed som default) ---
st.markdown("---")
with st.expander("⚙️ Innstillinger", expanded=False):
    st.write("Velg overraskelsestype:")
    cols = st.columns(3)
    opts = ["gif","image","css"]
    for i,opt in enumerate(opts):
        sel = (st.session_state.settings.get("type")==opt)
        if cols[i].checkbox(opt.upper(), value=sel, key=f"set_{opt}"):
            st.session_state.settings["type"] = opt
    # URL/CSS felter
    st.session_state.settings["gif"]   = st.text_input("GIF URL", value=st.session_state.settings.get("gif"))
    st.session_state.settings["image"] = st.text_input("Image URL", value=st.session_state.settings.get("image"))
    st.session_state.settings["css"]   = st.text_area("Custom CSS HTML", value=st.session_state.settings.get("css"))
    if st.button("Lagre innstillinger"):
        save_settings(st.session_state.settings)
        st.success("Innstillinger lagret!")
```
