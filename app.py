import streamlit as st 
from PIL import Image
from google import genai
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")

client=genai.Client(api_key=api_key)
st.title("Extract Text From Image")
user_input=st.file_uploader("choose an image",type=['jpg','png','jpeg'])
if user_input is not None:
    image=Image.open(user_input)
    st.image(image,caption="Uploaded Image",use_container_width=True)

    with open("temp_image.png","wb")as f:
        f.write(user_input.getbuffer())
        with st.spinner("Getting text from your image...."):
         file=client.files.upload(file="temp_image.png")
        
         response = client.models.generate_content(
         model="gemini-1.5-flash",
         contents=[{
            "role": "user",
            "parts": [
                {"fileData": {"fileUri": file.uri}},
                {"text": "Extract all text from this image"}
            ]
        }]
    )
         st.success("Extracted text successfully")
        st.subheader("Extracted Text: ")
        st.write(response.text)
        st.download_button(label="Download Extracted Text",data=response.text,file_name="ocr_output.txt",mime="text/plain")
        languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Bengali": "bn",
    "Urdu": "ur"

     }
        target_language=st.selectbox("Select language to convert",list(languages))
        if st.button("Translate Text"):
           translated_text=GoogleTranslator(source="auto",target=languages[target_language]).translate(response.text)
           st.write("Translated Text: ",translated_text)
        
else:
   st.write("Upload an image")
