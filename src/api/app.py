import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.api.predictor import HotelClusterPredictor
from src.api.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    HealthResponse,
    ModelInfoResponse,
)

logger = logging.getLogger(__name__)

predictor = HotelClusterPredictor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        predictor.load()
        logger.info("API startup completed successfully.")
    except Exception as e:
        logger.exception("Failed to initialize API: %s", e)
        raise
    yield
    logger.info("API shutdown completed.")


app = FastAPI(
    title="Hotel Cluster Recommendation API",
    description="Predicts the top 5 hotel clusters for a given search context.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", response_model=HealthResponse)
def root():
    return HealthResponse(
        status="ok",
        message="Hotel Cluster Recommendation API is running."
    )


@app.get("/health", response_model=HealthResponse)
def health():
    if not predictor.is_loaded():
        raise HTTPException(status_code=503, detail="Model is not loaded.")

    return HealthResponse(
        status="ok",
        message="Model loaded and API ready."
    )


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    try:
        info = predictor.get_model_info()
        return ModelInfoResponse(**info)
    except Exception as e:
        logger.exception("Failed to retrieve model info: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/example-payload")
def example_payload():
    return {
        "is_mobile": 1,
        "is_package": 0,
        "channel": 9,
        "cnt": 2,
        "trip_type": "solo",
        "is_family_trip": 0,
        "is_multi_room": 0,
        "total_guests": 1,
        "stay_duration": 3,
        "advance_booking_days": 12,
        "user_location_country": 66,
        "hotel_country": 50,
        "srch_destination_id": 8250,
        "srch_destination_type_id": 1,
        "distance_group": "medium",
        "is_distance_unknown": 0,
        "distance_clean": 250.0,
        "distance_behavior_group": "medium",
        "avg_session_intensity": 1.6,
        "avg_stay_duration": 4.2,
        "avg_advance_booking_days": 30.0,
        "mobile_usage_rate": 0.8,
        "destination_booking_rate": 0.12,
        "destination_popularity": 900
    }


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    try:
        result = predictor.predict_top5(request.model_dump())
        return RecommendationResponse(**result)
    except Exception as e:
        logger.exception("Prediction failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))