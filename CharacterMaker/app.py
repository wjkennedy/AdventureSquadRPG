import streamlit as st
from fpdf import FPDF
import tempfile
import os

# Constants
STAT_NAMES = ["Agility", "Strength", "Intelligence", "Charm", "Endurance"]
MAX_POINTS = 15

# UI
st.title("Adventure Squad RPG Character Sheet Builder")

name = st.text_input("Character Name")
animal_type = st.selectbox("Animal Type", ["Dog", "Cat", "Rabbit", "Fox", "Otter", "Other"])
primary_role = st.selectbox("Primary Role", ["Rescue Specialist", "Medic", "Inventor", "Explorer", "Scout"])
special_skill = st.text_input("Special Skill")
traits = st.text_area("Personality Traits")
equipment = st.text_area("Equipment")
backstory = st.text_area("Backstory")

st.subheader("Distribute 15 points among your stats")
points_allocated = 0
stats = {}
for stat in STAT_NAMES:
    value = st.number_input(f"{stat}:", min_value=0, max_value=MAX_POINTS, step=1, key=stat)
    stats[stat] = value
    points_allocated += value

points_left = MAX_POINTS - points_allocated
st.markdown(f"**Points Remaining: {points_left}**")
if points_left < 0:
    st.error("You've allocated more than 15 points. Please reduce some values.")

if st.button("Generate PDF") and points_left == 0:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Adventure Squad Character Sheet", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Animal Type: {animal_type}", ln=True)
    pdf.cell(200, 10, txt=f"Primary Role: {primary_role}", ln=True)
    pdf.cell(200, 10, txt=f"Special Skill: {special_skill}", ln=True)
    pdf.ln(5)

    pdf.cell(200, 10, txt="Personality Traits:", ln=True)
    pdf.multi_cell(0, 10, txt=traits)
    pdf.ln(2)

    pdf.cell(200, 10, txt="Stats:", ln=True)
    for stat, value in stats.items():
        pdf.cell(200, 10, txt=f"{stat}: {value}", ln=True)
    pdf.ln(2)

    pdf.cell(200, 10, txt="Equipment:", ln=True)
    pdf.multi_cell(0, 10, txt=equipment)
    pdf.ln(2)

    pdf.cell(200, 10, txt="Backstory:", ln=True)
    pdf.multi_cell(0, 10, txt=backstory)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        with open(tmpfile.name, "rb") as f:
            st.download_button("Download Character Sheet", f, file_name="character_sheet.pdf", mime="application/pdf")
        os.unlink(tmpfile.name)

