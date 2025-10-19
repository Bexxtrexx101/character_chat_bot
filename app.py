import streamlit as st
import requests

# UI
st.title("Character Chatbot")
notion_url = st.text_input("Paste your Notion character page URL:")

if notion_url:
    # Scrape Notion page content (public pages)
    page_content = requests.get(notion_url).text  # crude method, refine for rich text extraction

    # Prompt Engineering
    character_prompt = f"""
    You are a fictional character described as follows:
    [PAGE CONTENT]
    ---
    {page_content}
    ---
    Respond in this character's voice and context only.
    """

    user_input = st.text_input("Ask the character:")
    if user_input:
        # Send to free AI model, e.g., Hugging Face Inference API
        api_url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": "Bearer <YOUR_FREE_HF_TOKEN>"}
        payload = {"inputs": character_prompt + user_input}
        response = requests.post(api_url, headers=headers, json=payload)
        st.write(response.json())
