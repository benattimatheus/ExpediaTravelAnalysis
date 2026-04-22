from typing import Tuple
import pandas as pd


def load_model_data(engine) -> pd.DataFrame:
    """
    Load the modeling dataset from PostgreSQL using SQLAlchemy engine.
    """
    query = "SELECT * FROM gold_model_dataset"

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df


def temporal_split(
    df: pd.DataFrame,
    date_column: str = "date_time",
    test_size: float = 0.2
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split dataset temporally.
    Oldest records go to train, newest records go to test.
    """
    if date_column not in df.columns:
        raise ValueError(f"The modeling dataset must contain '{date_column}' for temporal split.")

    temp_df = df.copy()
    temp_df[date_column] = pd.to_datetime(temp_df[date_column], errors="coerce")
    temp_df = temp_df.dropna(subset=[date_column]).sort_values(date_column)

    split_index = int(len(temp_df) * (1 - test_size))

    train_df = temp_df.iloc[:split_index].copy()
    test_df = temp_df.iloc[split_index:].copy()

    return train_df, test_df


def prepare_features_and_target(
    df: pd.DataFrame,
    use_leakage_features: bool = True
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Prepare features and target for hotel cluster prediction.

    use_leakage_features=True:
        keeps user_booking_rate and cluster_booking_rate for portfolio-oriented experimentation.

    use_leakage_features=False:
        removes leakage-prone features for a more realistic setup.
    """
    df = df.copy()

    # remove critical null target rows
    df = df.dropna(subset=["hotel_cluster"])

    # base columns to remove from X
    columns_to_drop = [
        "hotel_cluster",
        "is_booking",   # not a feature for hotel_cluster prediction
        "date_time"     # used only for temporal split
    ]

    # leakage handling
    if not use_leakage_features:
        leakage_cols = [
            "user_booking_rate",
            "cluster_booking_rate",
            "cluster_popularity",
            "destination_booking_rate"
        ]
        columns_to_drop.extend([col for col in leakage_cols if col in df.columns])

    # remove raw distance if you prefer engineered versions;
    # here we keep both distance_clean and categorical groupings
    # and drop raw orig_destination_distance to reduce redundancy.
    optional_drop = [
        "orig_destination_distance"
    ]
    columns_to_drop.extend([col for col in optional_drop if col in df.columns])

    existing_to_drop = [col for col in columns_to_drop if col in df.columns]

    X = df.drop(columns=existing_to_drop)
    y = df["hotel_cluster"].astype(int)

    # convert categoricals to dummy variables
    categorical_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=False)

    # fill nulls conservatively
    X = X.fillna(-1)

    return X, y