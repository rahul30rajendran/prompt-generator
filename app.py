import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load your Groq API token
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="AI Prompt Generator", page_icon="✨")
st.title("✨ Prompt Generator Tool- by Rahul✨")

st.markdown("""
Describe a task, and this tool will generate a high-quality prompt using the LLaMA 3 model (via Groq API).
""")

# User input
task = st.text_area("🔍 Describe your task", placeholder="e.g., Summarize a research article")
tone = st.selectbox("🎭 Choose tone/style (optional)", ["Default", "Formal", "Casual", "Creative", "Academic"])
role = st.text_input("🧐 Specify AI role (optional)", placeholder="e.g., You are a legal expert")

if st.button("🚀 Generate Prompt"):
    if task.strip() == "":
        st.warning("Please enter a task description.")
    else:
        # Compose the full input prompt
        full_input = f"""
You are a helpful prompt engineer.
Generate a high-quality prompt for a language model based on this task:

Task: {task}
Tone/Style: {tone if tone != 'Default' else 'None'}
Role: {role if role else 'None'}

The prompt should:
- Specify the AI's role if provided
- Include clear instructions
- Suggest format (if needed)
- Match the tone
- Be useful to paste into ChatGPT or Claude
"""

        # Send to Groq API (OpenAI-compatible)
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful prompt engineer."},
                {"role": "user", "content": full_input.strip()}
            ]
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            output = response.json()
            result_text = output["choices"][0]["message"]["content"]
            st.subheader("📝 Suggested Prompt")
            st.code(result_text.strip(), language='markdown')
            st.success("Copy the above prompt into any AI tool!")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

