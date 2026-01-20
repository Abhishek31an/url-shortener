import streamlit as st
import requests
st.set_page_config(page_title="URL Shortener", page_icon="🔗")
BACKEND_URL = "https://my-url-shortener-yihr.onrender.com"
st.title("🔗 Professional URL Shortener")
st.write("Built with FastAPI (Backend) & Streamlit (Frontend)")
long_url = st.text_input("Enter your long URL here:", placeholder="https://www.google.com")

if st.button("Shorten URL"):
    if long_url:
        try:
            payload = {"url": long_url}
            response = requests.post(f"{BACKEND_URL}/shorten", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                short_key = data['short_key']
                
                full_short_link = f"{BACKEND_URL}/{short_key}"
                
                st.success("URL Shortened Successfully! 🎉")
                
                st.code(full_short_link, language="text")
                st.write(f"[Click here to visit]({full_short_link})")
                
                st.info(f"Original: {data['original_url']}")
                
            else:
                st.error("Error: Could not shorten URL. Server returned an error.")
                
        except Exception as e:
            st.error(f"Connection Error: {e}")
            st.warning("Note: Since the backend is on free hosting, it might be 'sleeping'. Try clicking the button again in 30 seconds.")
    else:
        st.warning("Please enter a URL first.")

with st.sidebar:
    st.header("About")
    st.markdown("""
    This app separates logic from design:
    - **Frontend:** Streamlit (Python)
    - **Backend:** FastAPI (Python)
    - **Database:** PostgreSQL (Neon)
    """)