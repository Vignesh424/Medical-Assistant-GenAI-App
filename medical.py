import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv,find_dotenv
from PIL import Image
load_dotenv()
genai.configure(api_key="AIzaSyBZUa2gpJGrSbOBzG23dE8LNhPmY4lgdrg") #PLEASE DONT COPY THE API KEY. GENERATE YOUR OWN AND USE IT


def get_gemini_response(input,image):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Gemini MedicalAssitant App")

st.header("Gemini MedicalAssitant App")
#input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Analyze the Image")

input_prompt="""You are a high skilled Medical Practitioner specialised in Image Analysis, you task includes the following

1. Detailed Analysis: Analyze the image, find minute details from the image about the person's suffering/problem. 
Analyze the image in such a way that minute details are not missed.

2. Findings: Describe the findings from the image i.e. the Symtoms, Causes and how the germs or bacteria might have entered the body 

3. Disease If Any: Name the disease which comes you your mind after analysis of the image.

4. Recommendation and Next Steps: Give a detailed recommendation on what is to be done next and what specialised 
tests need to be done, which medicines need to be taken for treatment
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.subheader("Here is your analysis of the image")
    st.write(response)

