
import streamlit as st
import json
import os

DATA_FILE = "data.json"
PERSONER = ["Anders", "Mattis", "Preben"]
MAX_OPPGAVER = 3

# Last eller initier data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {p: [] for p in PERSONER} | {"kpi": {p: 0 for p in PERSONER} | {"total": 0}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Legg til en ny oppgave
def legg_til_oppgave(data, person, tittel, beskrivelse):
    if len(data[person]) < MAX_OPPGAVER:
        data[person].append({
            "tittel": tittel,
            "beskrivelse": beskrivelse,
            "status": [False]*10,
            "venter": False,
            "ventetekst": ""
        })

# Streamlit UI
data = load_data()
st.set_page_config(page_title="Pågående oppgaver")
st.title("📋 Pågående oppgaver")

# KPI-visning
st.subheader("🔢 KPI-statistikk")
kpi_cols = st.columns(len(PERSONER) + 1)
kpi_cols[0].metric("Fullført totalt", data["kpi"]["total"])
for i, p in enumerate(PERSONER):
    kpi_cols[i+1].metric(f"{p} fullførte", data["kpi"][p])

st.markdown("---")

# Hovedvisning per person
for person in PERSONER:
    st.subheader(f"👤 {person}")
    person_section = st.container()

    # Vis aktive oppgaver
    nye_oppgaver = []
    for idx, oppgave in enumerate(data[person]):
        st.markdown(f"**{oppgave['tittel']}**  ")
        st.markdown(oppgave["beskrivelse"])

        # Progressbar med 10 bokser
        cols = st.columns(10)
        for i in range(10):
            if cols[i].checkbox("", value=oppgave["status"][i], key=f"{person}_{idx}_{i}"):
                oppgave["status"][i] = True

        # Beregn ferdigstillelse
        prosent = sum(oppgave["status"]) * 10
        st.progress(prosent)

        # "Venter på noen"
        with st.expander("⚠️ Venter på noen?"):
            vent = st.checkbox("Venter", value=oppgave["venter"], key=f"{person}_{idx}_venter")
            tekst = st.text_input("Kort kommentar", value=oppgave["ventetekst"], max_chars=30, key=f"{person}_{idx}_tekst")
            oppgave["venter"] = vent
            oppgave["ventetekst"] = tekst

        # Fjern oppgaver som er 100%
        if sum(oppgave["status"]) == 10:
            data["kpi"][person] += 1
            data["kpi"]["total"] += 1
        else:
            nye_oppgaver.append(oppgave)
        st.markdown("---")
    data[person] = nye_oppgaver

    # Legg til ny oppgave
    if len(data[person]) < MAX_OPPGAVER:
        with st.form(f"form_{person}"):
            st.markdown("*Ny oppgave*")
            tittel = st.text_input("Tittel", key=f"{person}_tittel")
            beskrivelse = st.text_area("Beskrivelse", key=f"{person}_beskrivelse")
            submitted = st.form_submit_button("Legg til")
            if submitted and tittel:
                legg_til_oppgave(data, person, tittel, beskrivelse)
                st.success("Oppgave lagt til")
                st.rerun()

save_data(data)
