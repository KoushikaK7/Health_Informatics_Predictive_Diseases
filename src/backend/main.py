from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from logging import getLogger
from ml.services import predict, Filter, predict_diabetes
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of origins that are allowed (can be ["*"] for all)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.mount("/backend/figures", StaticFiles(directory="figures"), name="static")


_logger = getLogger(__name__)

# Load the data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data/country-state-county.csv')
df = pd.read_csv(DATA_PATH)


@app.get("/states/{country_name}")
def get_state(country_name: str):
    """
    Returns a list of states for a given country.
    """
    # Filter the DataFrame for the given country and drop duplicates
    states = df[df['country_name'].str.lower() == country_name.lower()]['state_name'].drop_duplicates().tolist()
    return {"country": country_name, "states": states}


@app.get("/counties/{state_name}")
def get_county(state_name: str):
    """
    Returns a list of counties for a given state.
    """
    # Filter the DataFrame for the given state and drop duplicates
    counties = df[df['state_name'].str.lower() == state_name.lower()]['county_name'].drop_duplicates().tolist()
    return {"state": state_name, "counties": counties}


@app.post('/generate')
def predict_outbreak(filter_data: Filter):
    try:
        print(filter_data)
        image_names = []
        if filter_data.disease == 'COVID':
            image_names = predict(filter_data)
        else:
            print(filter_data.disease)
            image_names = predict_diabetes(filter_data)

        image_urls = [f"../backend/figures/{name}" for name in image_names]

        return JSONResponse(content={
            "response": "OK",
            "data": "Image saved successfully under src/backend/figures",
            "image_urls": image_urls
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
