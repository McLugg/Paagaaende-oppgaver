
import streamlit as st
import json
import uuid
import os

st.set_page_config(page_title="Oppgaveliste", layout="centered")

DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"oppgaver": [], "fullfort": []}, f)

with open(DATA_FILE, "r") as f:
    data = json.load(f)

# Inspirasjon fra retro spillstil: grønn bar med pixel-feel og AI-belønning
def vis_fremdriftsbar(prosent, oppgave_id):
    bar_length = 20
    fylte = int(prosent / 100 * bar_length)
    tomme = bar_length - fylte
    pixel_bar = "🟩" * fylte + "⬛" * tomme
    st.markdown(f"**Fremdrift:** {pixel_bar} {prosent}%")

    nytt_prosent = st.slider(
        "Dra for å oppdatere fremdrift",
        0,
        100,
        prosent,
        step=10,
        key=f"slider_{oppgave_id}"
    )
    return nytt_prosent

st.title("Mine oppgaver")

# 2. Vise oppgaver før skjema
st.subheader("Pågående oppgaver")

for oppgave in data["oppgaver"]:
    st.markdown(f"### {oppgave['tittel']}")
    if oppgave.get("venter") and oppgave.get("kommentar"):
        st.info(f"🕒 Venter på: {oppgave['kommentar']}")
    nytt_prosent = vis_fremdriftsbar(oppgave["status"], oppgave["id"])

    if nytt_prosent != oppgave["status"]:
        oppgave["status"] = nytt_prosent
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        if nytt_prosent == 100:
            belonning = st.chat_message("ai", avatar="🤖")
            belonning.write("💥 BOOM! Oppgaven din er DONE! Helt rått!")
            data["fullfort"].append(oppgave)
            data["oppgaver"] = [o for o in data["oppgaver"] if o["id"] != oppgave["id"]]
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=2)
            st.experimental_rerun()

# 1. Skjema for ny oppgave nederst
st.subheader("Legg til ny oppgave")
with st.form("ny_oppgave"):
    ny_tittel = st.text_input("Hva skal gjøres?", key="new_title")
    ny_venter = st.checkbox("Venter på noen?", key="new_wait")
    ny_kommentar = ""
    if ny_venter:
        ny_kommentar = st.text_area("Hva venter du på?", key="new_comment")
    legg_til = st.form_submit_button("Legg til oppgave")
    if legg_til:
        ny = {
            "id": str(uuid.uuid4()),
            "tittel": ny_tittel,
            "venter": ny_venter,
            "kommentar": ny_kommentar,
            "status": 0
        }
        data["oppgaver"].append(ny)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        st.success("Oppgave lagt til!")
        st.experimental_rerun()

# 3. Vis KPI
st.subheader("📊 Fremdrift")
totalt = len(data["oppgaver"]) + len(data["fullfort"])
ferdig = len(data["fullfort"])
snitt_tid = "N/A"
st.metric("Totalt", totalt)
st.metric("Ferdige", ferdig)
st.metric("Snitt tid", snitt_tid)
