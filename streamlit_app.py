# streamlit_intake.py
import streamlit as st
import json

# --- Load JSON files (from the same directory) ---
@st.cache_data
def load_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

symptoms = load_json("infermedica_symptoms.json")
risk_factors = load_json("infermedica_risk_factors.json")
conditions = load_json("infermedica_conditions.json")

symptom_names = [s["name"] for s in symptoms]
symptom_name_to_id = {s["name"]: s["id"] for s in symptoms}

risk_names = [r["name"] for r in risk_factors]
risk_name_to_id = {r["name"]: r["id"] for r in risk_factors}

cond_names = [c["name"] for c in conditions]
cond_name_to_id = {c["name"]: c["id"] for c in conditions}

# --- Streamlit Layout ---
st.title("Patient Intake Form")

st.subheader("Patient Details")
sex = st.selectbox("Sex", ["female", "male"])
age = st.number_input("Age", min_value=0, max_value=120, value=30)

st.subheader("Chief Complaint")
chief_complaint = st.text_area("Enter patient's chief complaint")

st.subheader("Symptoms")
selected_symptoms = st.multiselect("Search & select symptoms", symptom_names)

st.subheader("Risk Factors")
selected_risk = st.multiselect("Search & select risk factors", risk_names)

st.subheader("Chronic / Existing Conditions")
selected_conditions = st.multiselect("Search & select chronic conditions", cond_names)

if st.button("Generate Summary"):
    # Generate human-readable summary
    summary = f"Patient Summary:\n\nSex: {sex}\nAge: {age}\n\n"
    if chief_complaint:
        summary += f"Chief Complaint: {chief_complaint}\n\n"
    if selected_symptoms:
        summary += "Symptoms:\n- " + "\n- ".join(selected_symptoms) + "\n\n"
    if selected_risk:
        summary += "Risk Factors:\n- " + "\n- ".join(selected_risk) + "\n\n"
    if selected_conditions:
        summary += "Chronic/Existing Conditions:\n- " + "\n- ".join(selected_conditions) + "\n"

    st.subheader("Patient Summary")
    st.text(summary)

    # Optionally, generate JSON payload (hidden)
    payload = {
        "sex": sex,
        "age": age,
        "symptoms": [{"id": symptom_name_to_id[n], "choice_id": "present"} for n in selected_symptoms],
        "risk_factors": [risk_name_to_id[n] for n in selected_risk],
        "chronic_conditions": [cond_name_to_id[n] for n in selected_conditions]
    }
