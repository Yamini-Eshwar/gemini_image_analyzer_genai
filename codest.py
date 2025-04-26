import streamlit as st
import google.generativeai as genai
import os
import io
import base64
from PIL import Image

st.set_page_config(page_title="GeminiAI Image Analyzer", layout="wide", page_icon="🧠")

st.markdown(
    """
    <style>
    .stApp{
        background-image: url("https://images.unsplash.com/photo-1677756119517-756a188d2d94?q=80&w=2050&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size:cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
      }

      .transparent-box{
        background-color: rgba(255,255,255,0.6);
        padding:20px;
        font-family:Roboto;
        font-size: 17px;
        color: #4d5054;
        border-radius: 15px;
        margin-top: 20px;
      }
      h1 {
        text-align: center;
        font-size: 3em;
        color: #ffffff;
        text-shadow: 2px 2px 8px #000;
      }
    </style>
    """, unsafe_allow_html=True)

# Fetch the API key securely from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

st.title("GeminiAI Image Analyzer")
st.sidebar.title("🔍 Select Model")

st.sidebar.markdown(
    """
    <style>
      div[data-baseweb="select"] > div{
        border: 2px solid #00ff00 !important; /* Green Border */
        box-shadow: 0 0 10px #00ff00; /* Green Glow */
        border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

model_options = st.sidebar.selectbox("choose a Gemini model", [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods])


st.markdown("<p style='color: #ffffff; font-size: 18px; font-weight:bold;font-family:Roboto;'>Upload an image and get an AI-powered description</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    with st.spinner('Loading your image...'):
        img = Image.open(uploaded_file)
        st.image(img)
        st.markdown("""
        <style>
          @keyframes fadeIn {
          from {opacity: 0;}
          to {opacity:1;}
          }
          .caption {
          text-align: center;
          color: #ffffff;
          font-size: 20px;
          font-family: Monospace;
          font-weight: bold;
          animation: fadeIn 2s;
          }
        </style>

        <p class='caption'>✨ Uploaded Image ✨</p>
        """, unsafe_allow_html=True)

    buffered = io.BytesIO()
    img = img.convert("RGB")
    img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

model = genai.GenerativeModel(model_options)

try:     
    response = model.generate_content([img, "Describe this image."])

    st.markdown(f""""
                  <div class="transparent-box"> 
                    <h3>Image Description: {response.text} </h3>
                  </div> 
                  """, unsafe_allow_html=True)
      
except Exception as e:
    st.error(f"Error: {str(e)}")

else:
    st.warning("Please upload an image to proceed.")

