import logging
from pathlib import Path
from typing import Dict, Any, List
import joblib
import numpy as np
import pandas as pd

from src.api.utils import payload_to_dataframe, align_features

logger = logging.getLogger(__name__)

MODEL_PATH = Path("artifacts/models/lgbm_hotel_cluster.joblib")


class HotelClusterPredictor:
    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.feature_names: List[str] = []
        self.classes_: List[int] = []

    def load(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at '{self.model_path}'. Train the model first."
            )

        logger.info("Loading model from %s", self.model_path)
        self.model = joblib.load(self.model_path)

        if not hasattr(self.model, "feature_name_"):
            raise AttributeError("Loaded model does not expose feature_name_.")

        if not hasattr(self.model, "classes_"):
            raise AttributeError("Loaded model does not expose classes_.")

        self.feature_names = list(self.model.feature_name_)
        self.classes_ = [int(c) for c in self.model.classes_]

        logger.info(
            "Model loaded successfully. Features: %s | Classes: %s",
            len(self.feature_names),
            len(self.classes_),
        )

    def is_loaded(self) -> bool:
        return self.model is not None

    def get_model_info(self) -> Dict[str, Any]:
        if not self.is_loaded():
            raise RuntimeError("Model is not loaded.")

        return {
            "model_type": type(self.model).__name__,
            "n_features": len(self.feature_names),
            "n_classes": len(self.classes_),
            "feature_names": self.feature_names,
        }

    def _prepare_input(self, payload: Dict[str, Any]) -> pd.DataFrame:
        if not self.is_loaded():
            raise RuntimeError("Model is not loaded.")

        df = payload_to_dataframe(payload)
        df = align_features(df, self.feature_names)
        return df

    def predict_top5(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return top-5 predicted hotel clusters and their scores.
        """
        if not self.is_loaded():
            raise RuntimeError("Model is not loaded.")

        X = self._prepare_input(payload)
        probs = self.model.predict_proba(X)

        top5_idx = np.argsort(probs[0])[-5:][::-1]

        predictions = []
        top_5_hotel_clusters = []

        for idx in top5_idx:
            cluster = int(self.classes_[idx])
            score = float(probs[0][idx])

            top_5_hotel_clusters.append(cluster)
            predictions.append(
                {
                    "hotel_cluster": cluster,
                    "score": round(score, 6),
                }
            )

        return {
            "top_5_hotel_clusters": top_5_hotel_clusters,
            "predictions": predictions,
        }