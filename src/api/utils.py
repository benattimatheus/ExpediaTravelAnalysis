import logging
from typing import Dict, Any
import pandas as pd

logger = logging.getLogger(__name__)


def payload_to_dataframe(payload: Dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame([payload])


def align_features(df: pd.DataFrame, feature_names: list[str]) -> pd.DataFrame:
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=False)
    df = df.fillna(-1)
    df = df.reindex(columns=feature_names, fill_value=0)
    return df