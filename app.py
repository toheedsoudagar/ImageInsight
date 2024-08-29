import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
 
# Define your Google API key directly
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
 
## Let's create a function to load Gemini Pro Vision
model = genai.GenerativeModel('gemini-1.5-flash')
 
def get_gemini_response(input, image, prompt):
    if input==None:
        input = "Give hidden insight on the image"
    response = model.generate_content([input, image[0], prompt])
    return response.text
 
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
       
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
 
## Initialize User Interface by using streamlit
st.set_page_config(page_title="Nu-Pie Image Insights Generator")
st.header("Nu-pie Image Insights Generator Application")
input = st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose an Image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
 
submit = st.button("Give insights on the Image")
 
input_prompt = """
You are an expert in understanding and providing Insights on Dashboard Images in detail.
We will upload an image of a PowerBi Dashboard and you will have to answer any questions related to that uploaded image.
"""
 
# If submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)
