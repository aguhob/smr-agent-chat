import streamlit as st
from openai import OpenAI
import json

st.set_page_config(page_title="🎙️ Voice Risk Assistant")
st.title("🎙️ Developer Risk Voice Assistant")
st.markdown("Speak or type your concern and get an AI-generated risk insight, enhanced with local data and community feedback.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Load enhanced risk data
try:
    with open("enhanced_risk_data.json", "r") as f:
        enhanced_data = json.load(f)
except FileNotFoundError:
    enhanced_data = {}

# Placeholder agent outputs from earlier pipeline
agent1_output = "SMRs may face local permitting resistance in flood-prone zones."
agent2_output = "Key risks: Environmental flooding, regulatory delays."
agent3_output = "Mitigation: Engage early with local water boards and initiate pre-permitting assessments."

# Voice input disabled — fallback to text input
transcript = st.text_input("Type your question or concern here:", "What risks should I watch for in San Antonio?")

# Extract location if mentioned in voice (or ask user to specify)
location = st.text_input("Which city or region are you referring to?", "San Antonio")

# Fetch community feedback from Airtable
try:
    import requests
    airtable_api_key = st.secrets["AIRTABLE_API_KEY"]
    base_id = st.secrets["AIRTABLE_BASE_ID"]
    table_name = st.secrets["AIRTABLE_TABLE_NAME"]
    airtable_url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    headers = {"Authorization": f"Bearer {airtable_api_key}"}
    params = {"filterByFormula": f"SEARCH(\"{location}\", {{City}})"}
    res = requests.get(airtable_url, headers=headers, params=params)
    community_records = res.json().get("records", [])
    community_feedback = "
".join([rec["fields"].get("Concern", "") for rec in community_records]) or "No recent community feedback."
except Exception as e:
    community_feedback = "Could not load community feedback."

# Merge data for assistant context
city_context = enhanced_data.get(location, [])
