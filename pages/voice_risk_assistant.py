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
"  # fixed unterminated string.join([rec["fields"].get("Concern", "") for rec in community_records]) or "No recent community feedback."
except Exception as e:
    community_feedback = "Could not load community feedback."

# Merge data for assistant context
city_context = enhanced_data.get(location, [])
community_feedback = "Recent concerns include permitting delays and water usage impacts."

combined_context = f"""
Strategic Advisory: {agent1_output}
Risk Summary: {agent2_output}
Mitigation Plan: {agent3_output}

Local Intelligence:
{json.dumps(city_context, indent=2)}

Community Feedback:
{community_feedback}
"""

# GPT response
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful and clear risk mitigation advisor for energy projects."},
        {"role": "user", "content": f"User asked: '{transcript}'\\n\\nContext:\\n{combined_context}"}
    ]
)

reply = response.choices[0].message.content
st.markdown(f"**AI Assistant says:** {reply}")

# Optional: Play voice response with ElevenLabs
try:
    import base64
    import requests
    elevenlabs_api_key = st.secrets["ELEVENLABS_API_KEY"]
    voice = "Rachel"  # or any available ElevenLabs voice
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    headers = {
        "xi-api-key": elevenlabs_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": reply,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        audio_bytes = response.content
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.warning("Could not generate audio response.")
except Exception as e:
    st.info("Voice playback not available. Make sure ELEVENLABS_API_KEY is set in secrets.")

st.markdown("---")
st.markdown("### 📝 Want a full project report?")
st.markdown("[Return to the PDF generator form](./Home)")
