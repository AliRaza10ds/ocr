import streamlit as st 
from PIL import Image
# Correct import for the Google Generative AI library
import google.generativeai as genai
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure the Generative AI library with the API key
genai.configure(api_key=api_key)

# Initialize the Gemini model for content generation
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Extract Text From Image")
st.markdown("This app extracts text from an image and can translate it to various languages.")

# File uploader to choose an image
user_input = st.file_uploader("Choose an image", type=['jpg', 'png', 'jpeg'])

# Proceed if an image is uploaded
if user_input is not None:
    # Open the uploaded image using Pillow
    image = Image.open(user_input)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Use a Streamlit spinner to show that text extraction is in progress
    with st.spinner("Getting text from your image..."):
        try:
            # Generate content using the model. We pass the PIL Image object directly.
            
            response = model.generate_content([
                {"text": "Extract all text from this image"},
                image
            ])
            st.success("Extracted text successfully!")
            
            # Display the extracted text
            st.subheader("Extracted Text:")
            st.write(response.text)
            
            # Download button for the extracted text
            st.download_button(
                label="Download Extracted Text",
                data=response.text,
                file_name="ocr_output.txt",
                mime="text/plain"
            )

            # Language selection for translation
            languages = {
                "English": "en", "Hindi": "hi", "French": "fr", "German": "de",
                "Spanish": "es", "Chinese (Simplified)": "zh-CN", "Japanese": "ja",
                "Korean": "ko", "Arabic": "ar", "Russian": "ru", "Portuguese": "pt",
                "Italian": "it", "Bengali": "bn", "Urdu": "ur"
            }
            target_language = st.selectbox("Select language to translate to", list(languages.keys()))
            
            # Translate button
            if st.button("Translate Text"):
                translated_text = GoogleTranslator(
                    source="auto",
                    target=languages[target_language]
                ).translate(response.text)
                st.subheader("Translated Text:")
                st.write(translated_text)
                
        except Exception as e:
            # Handle any potential errors during the API call
            st.error("an error occured..please ensure image is in correct format")
            
else:
    # Message to display if no image is uploaded
    st.write("Upload an image to get started.")
