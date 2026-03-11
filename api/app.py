import os
from contextlib import asynccontextmanager
from typing import List, Tuple

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import mlflow

load_dotenv()

MLFLOW_URI = os.environ["MLFLOW_URI"]
EXPERIMENT_NAME = "getaround"

MODEL_ID = "m-83c8393e7ac14d7b9fa37c31b525cc00"  # GradientBoostingRegressor_model

FEATURE_NAMES = [
    "model_key",
    "mileage",
    "engine_power",
    "fuel",
    "paint_color",
    "car_type",
    "private_parking_available",
    "has_gps",
    "has_air_conditioning",
    "automatic_car",
    "has_getaround_connect",
    "has_speed_regulator",
    "winter_tires",
]

description = """
Ensemble des endpoints de l'API Getaround
"""

tags_metadata = [
    {
        "name": "Getaround API Endpoints",
        "description": "Getaround API endpoints",
    }
]


CarTuple = Tuple[
    str,  # model_key
    int,  # mileage
    int,  # engine_power
    str,  # fuel
    str,  # paint_color
    str,  # car_type
    bool,  # private_parking_available
    bool,  # has_gps
    bool,  # has_air_conditioning
    bool,  # automatic_car
    bool,  # has_getaround_connect
    bool,  # has_speed_regulator
    bool,  # winter_tires
]


class PredictRequest(BaseModel):
    input: List[CarTuple]

    model_config = {
        "json_schema_extra": {
            "example": {
                "input": [
                    [
                        "Citroen",
                        234365,
                        135,
                        "diesel",
                        "black",
                        "estate",
                        True,
                        True,
                        False,
                        False,
                        True,
                        False,
                        True,
                    ],
                    [
                        "Volkswagen",
                        57344,
                        70,
                        "diesel",
                        "grey",
                        "hatchback",
                        False,
                        True,
                        False,
                        False,
                        False,
                        False,
                        True,
                    ],
                ]
            }
        }
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)
    app.state.model = mlflow.sklearn.load_model(f"models:/{MODEL_ID}")
    yield


app = FastAPI(
    title="Getaround API  Endpoints",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)


@app.get("/", tags=["Endpoints"], response_class=HTMLResponse, include_in_schema=False)
async def root():
    message = "La documentation de l'API est disponible a cette url :  <a href='docs'>`/docs`<a/>"
    return message


@app.post("/predict", tags=["Machine Learning"])
async def predict(input: PredictRequest):
    """
    Permet de prédire le prix journalier optimal d'une location de véhicule
    """

    input_data = input.input
    input_df = pd.DataFrame(input_data, columns=FEATURE_NAMES)

    model = app.state.model
    prediction = model.predict(input_df)

    return {"prediction": prediction.tolist()}
