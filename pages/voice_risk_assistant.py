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
        {"role": "user", "content": f"User asked: '{transcript}'\n\nContext:\n{combined_context}"}
    ]
)

reply = response["choices"][0]["message"]["content"]
st.markdown(f"**AI Assistant says:** {reply}")

st.markdown("---")
st.markdown("### 📝 Want a full project report?")
st.markdown("[Return to the PDF generator form](./Home)")
