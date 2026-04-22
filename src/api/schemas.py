from pydantic import BaseModel, Field
from typing import List, Optional


class RecommendationRequest(BaseModel):
    is_mobile: int = Field(..., ge=0, le=1)
    is_package: int = Field(..., ge=0, le=1)
    channel: int = Field(..., ge=0)
    cnt: int = Field(..., ge=0)

    trip_type: str
    is_family_trip: int = Field(..., ge=0, le=1)
    is_multi_room: int = Field(..., ge=0, le=1)
    total_guests: int = Field(..., ge=1)

    stay_duration: int = Field(..., ge=1)
    advance_booking_days: int = Field(..., ge=0)

    user_location_country: int = Field(..., ge=0)
    hotel_country: int = Field(..., ge=0)
    srch_destination_id: int = Field(..., ge=0)
    srch_destination_type_id: int = Field(..., ge=0)

    distance_group: str
    is_distance_unknown: int = Field(..., ge=0, le=1)
    distance_clean: Optional[float] = None
    distance_behavior_group: str

    avg_session_intensity: Optional[float] = -1
    avg_stay_duration: Optional[float] = -1
    avg_advance_booking_days: Optional[float] = -1
    mobile_usage_rate: Optional[float] = -1

    destination_booking_rate: Optional[float] = -1
    destination_popularity: Optional[float] = -1


class ClusterPrediction(BaseModel):
    hotel_cluster: int
    score: float


class RecommendationResponse(BaseModel):
    top_5_hotel_clusters: List[int]
    predictions: List[ClusterPrediction]


class HealthResponse(BaseModel):
    status: str
    message: str


class ModelInfoResponse(BaseModel):
    model_type: str
    n_features: int
    n_classes: int
    feature_names: List[str]