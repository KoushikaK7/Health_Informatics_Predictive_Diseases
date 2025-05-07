import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
import pandas as pd

# Define the URL of the FastAPI server
API_URL = "http://localhost:8000/generate"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Streamlit page layout
st.set_page_config(layout="wide")
# st.markdown(
#     """
#     <style>
#     .reportview-container {
#         background: white;
#     }
#     .sidebar .sidebar-content {
#         background: white;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
df = pd.read_csv('./country-state-county.csv')

# Creating the sidebar for input controls
with st.sidebar:
    st.title("Filter options")
    country = st.selectbox("Select a country:", df['country_name'].unique())

    filtered_df_country = df[df['country_name'] == country]

    selected_state = st.selectbox('Select a State:', filtered_df_country['state_name'].unique())

    filtered_df_state = filtered_df_country[filtered_df_country['state_name'] == selected_state]
    selected_county = st.selectbox('Select a County:', filtered_df_state['county_name'].unique())
    disease = st.selectbox("Select a disease:", ['COVID-19', 'HIV', 'Dengue'])
    submit_button = st.button("Submit")

# Main panel where content is shown
if submit_button:
    # Prepare the data for the POST request
    data = {
        "country": country,
        "state": selected_state,
        "county": selected_county,
        "disease": disease
    }

    # Send a POST request to the FastAPI backend
    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        # Assume the response contains a direct link to the image
        print("Current Working Directory:", os.getcwd())
        image_url = response.json().get('image_url')
        image_path = BASE_DIR + '/' + image_url
        print(image_path)
        # image_response = requests.get(image_url)
        #
        # if image_response.status_code == 200:
        #     # Load the image and display it
        #     image = Image.open(BytesIO(image_response.content))
        st.image(image_path, caption=f"Prediction for cases in {selected_state}:{selected_county}", use_column_width=True)
        # else:
        #     st.error("Failed to load image from the server.")
    else:
        st.error("Failed to retrieve data from the server.")
