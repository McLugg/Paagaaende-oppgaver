import streamlit as st
import json
import os
import random
import uuid

# --- Konstanter og filstier ---
DATA_FILE = "tasks.json"
STATS_FILE = "stats.json"

# Her definerer du ditt «flyvende symbol» som blir brukt i marquee-banneren.
# Du kan sette det til en enkel emoji, et HTML-bilde, eller en span med CSS-styling.
FLY_SYMBOL = "✈️"  # <-- Legg til denne linjen

# Surprise-eksempler: bytt enkelt her
SURPRISE_GIF = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmRuMWJxdmhzaHU4Z2Myd3g5bXZsaWRnMDJ6eHNjZnZyNmt3d3NhdiZhc29hdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tPplGWjN0xLybiU/giphy.gif"
SURPRISE_IMAGE = "https://imgflip.com/i/9uj9l8"
SURPRISE_CSS_BANNER = """
<style>
@keyframes glow {
  0% { text-shadow: 0 0 5px #5FAA58; }
  50% { text-shadow: 0 0 20px #80c372; }
  100% { text-shadow: 0 0 5px #5FAA58; }
}
.glow-banner {
  font-family: 'Press Start 2P', monospace;
  font-size: 24px; color: #5FAA58;
  animation: glow 1.5s infinite;
  text-align: center;
  margin: 16px 0;
}
</style>
<div class="glow-banner">
  🕹 LEVEL UP! YOU DID IT! 🕹
</div>
"""

# Velg hvilken overraskelse som vises ved fullføring
SURPRISE_HTML = f"""
<div style="text-align:center; margin:16px 0;">
  <img src="{SURPRISE_GIF}" alt="Surprise GIF" width="200" />
</div>
"""

# --- Motivasjonsmeldinger ved 25%, 50%, 75% og 100% ---
MOTIVATION = {
    25: ["💥 God start! Du er ¼ på vei!", "🚀 25% allerede – imponert!"],
    50: ["🏆 Halveis! Stå på videre!", "⭐ 50% – du ruller det inn!"],
    75: ["🔥 75% – nå er du nesten i mål!", "💪 ¾ gjort – fullfør det!"],
    100: ["🎉 WOW – du fullførte oppgaven!", "🥳 Fantastisk jobb – oppgave slaktet!"],
}

# … resten av koden uendret … 

def on_slider_change(task_id: str):
    task = next((t for t in st.session_state.tasks if t["id"] == task_id), None)
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
            # Vis overraskelse ved fullføring
            st.markdown(SURPRISE_HTML, unsafe_allow_html=True)
            # Ekstra feiring hver 5. fullførte oppgave
            if st.session_state.completed_count % 5 == 0:
                st.success(f"✨ Du har fullført {st.session_state.completed_count} oppgaver! ✨")
                # Her brukes FLY_SYMBOL – nå vil det ikke gi feil lenger:
                st.markdown(
                    f"""
                    <marquee behavior="smooth" direction="left" scrollamount="15">
                      <span style="font-size:48px;">{FLY_SYMBOL}</span>
                    </marquee>
                    """, unsafe_allow_html=True
                )

# … resten av koden videre …
