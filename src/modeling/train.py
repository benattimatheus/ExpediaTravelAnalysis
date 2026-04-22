import logging
import os
import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier

from src.modeling.dataset import (
    load_model_data,
    temporal_split,
    prepare_features_and_target
)
from src.modeling.metrics import mapk

logger = logging.getLogger(__name__)


def train_baseline(
    y_train: pd.Series,
    y_test: pd.Series,
    k: int = 5
) -> float:
    """
    Baseline using the top-k most frequent hotel clusters from the training set.
    """
    top_clusters = y_train.value_counts().index[:k].tolist()
    baseline_predictions = [top_clusters for _ in range(len(y_test))]
    baseline_score = mapk(y_test.tolist(), baseline_predictions, k=k)

    logger.info("Baseline MAP@%s: %.5f", k, baseline_score)
    return baseline_score


def train_lightgbm_classifier(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    model_output_path: str = "artifacts/models/lgbm_hotel_cluster.joblib",
    k: int = 5,
    use_leakage_features: bool = True
) -> dict:
    """
    Train a LightGBM multiclass classifier and evaluate with MAP@K.
    """
    X_train, y_train = prepare_features_and_target(
        train_df,
        use_leakage_features=use_leakage_features
    )
    X_test, y_test = prepare_features_and_target(
        test_df,
        use_leakage_features=use_leakage_features
    )

    # align train/test columns after dummy encoding
    X_train, X_test = X_train.align(X_test, join="left", axis=1, fill_value=0)

    num_classes = int(y_train.nunique())

    logger.info("Training LightGBM classifier.")
    logger.info("Train shape: %s | Test shape: %s", X_train.shape, X_test.shape)
    logger.info("Number of classes: %s", num_classes)
    logger.info("Leakage-prone features enabled: %s", use_leakage_features)

    model = LGBMClassifier(
        objective="multiclass",
        num_class=num_classes,
        n_estimators=300,
        learning_rate=0.05,
        num_leaves=31,
        max_depth=-1,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)
    classes = model.classes_

    topk_idx = np.argsort(probs, axis=1)[:, -k:][:, ::-1]
    topk_preds = [[int(classes[idx]) for idx in row] for row in topk_idx]

    model_score = mapk(y_test.tolist(), topk_preds, k=k)
    baseline_score = train_baseline(y_train, y_test, k=k)

    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(model, model_output_path)

    logger.info("Model MAP@%s: %.5f", k, model_score)
    logger.info("Saved model to %s", model_output_path)

    return {
        "baseline_mapk": baseline_score,
        "model_mapk": model_score,
        "train_rows": len(train_df),
        "test_rows": len(test_df),
        "n_features": X_train.shape[1],
        "n_classes": num_classes,
        "use_leakage_features": use_leakage_features,
        "model_path": model_output_path
    }


def run_model_training(
    engine,
    model_output_path: str = "artifacts/models/lgbm_hotel_cluster.joblib",
    #use_leakage_features: bool = True
    use_leakage_features: bool = False
) -> dict:
    """
    Full modeling pipeline:
    1. Load dataset from database
    2. Apply temporal split
    3. Train model
    4. Evaluate with MAP@5
    """
    logger.info("Loading modeling dataset from database.")
    df = load_model_data(engine)

    if "date_time" not in df.columns:
        raise ValueError(
            "The modeling dataset must contain 'date_time' for temporal split."
        )

    train_df, test_df = temporal_split(df, date_column="date_time", test_size=0.2)

    results = train_lightgbm_classifier(
        train_df=train_df,
        test_df=test_df,
        model_output_path=model_output_path,
        k=5,
        use_leakage_features=use_leakage_features
    )

    logger.info("Training complete. Results: %s", results)
    return results