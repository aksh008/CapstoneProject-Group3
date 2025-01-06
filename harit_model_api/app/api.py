import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import json
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from harit_model import __version__ as model_version
from harit_model.predict import make_prediction
from fastapi import FastAPI, UploadFile, File
import shutil


from app import __version__, schemas
# from app.config import settings

api_router = APIRouter()


# @api_router.get("/health", response_model=schemas.Health, status_code=200)
# def health() -> dict:
#     """
#     Root Get
#     """
#     health = schemas.Health(
#         name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
#     )

#     return health.dict()


UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)  # Create directory if it doesn't exist

@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: UploadFile = File(...)) -> Any:
    """
    Plant predictions with the harit_model
    """    
    # Read the image content
    #contents = await input_data.read()
    
    
    file_path = UPLOAD_DIR / input_data.filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(input_data.file, buffer)
        
    results = make_prediction(file_path)

    #if results["errors"] is not None:
    #    raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    return schemas.PredictionResults(
        errors="",
        version="",
        predictions=results)