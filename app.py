import streamlit as st
import requests
from bs4 import BeautifulSoup

# Get Hugging Face API token securely from Streamlit secrets
hf_token = st.secrets["hf_token"]

def scrape_notion_page(url):
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Combine main header, subheaders, paragraphs, and list items
        contents = ' '.join([el.get_text(separator=' ', strip=True)
                             for el in soup.find_all(['h1', 'h2', 'h3', 'p', 'li'])])
        return contents[:2000]  # Keep to 2000 characters for efficiency
    except Exception as e:
        return f"Failed to fetch Notion page: {e}"

st.title("Character Page AI Chatbot")

notion_url = st.text_input("Paste your public Notion character page URL:", "")
if notion_url:
    notion_content = scrape_notion_page(notion_url)
    st.write("Character memory found on this page:")
    st.info(notion_content[:800] + ("..." if len(notion_content) > 800 else ""))

    user_input = st.text_input("Ask your character a question:")

    if user_input:
        prompt = (
            "You are a fictional character. Base your answers only on this information:\n"
            f"{notion_content}\n"
            f"The user asks: {user_input}\n"
            "Stay in character!"
        )
        api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {
            "Authorization": f"Bearer {hf_token}"
        }
        payload = {"inputs": prompt}
        result = requests.post(api_url, headers=headers, json=payload)

        try:
            if result.status_code == 200 and isinstance(result.json(), list):
                model_reply = result.json()[0]['generated_text']
            else:
                model_reply = result.json().get('error', 'API error.')
        except Exception as e:
            model_reply = f"Error: {e}"
        st.success(model_reply)
