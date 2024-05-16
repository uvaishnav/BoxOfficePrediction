from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir : Path
    dataset_name : str
    ticket_price_dataset_link : str
    ticket_price_file : Path
    local_data_file : Path
    unzip_dir : Path

@dataclass(frozen=True)
class DataOrganizeConfig:
    movie_table_path : Path
    credit_table_path : Path
    ticket_price_table_path : Path
    org_table_path : Path

@dataclass(frozen=True)
class DataValidatioinConfig:
    root_dir : Path
    val_data_path : Path
    all_schema : dict
    status_file : Path

@dataclass(frozen=True)
class FeatureEngineeringConfig:
    organized_data : Path
    featured_data : Path
    scores_data : Path

@dataclass(frozen=True)
class DataPreprocessorConfig:
    root_dir : Path

@dataclass(frozen=True)
class ModelTrainingConfig:
    train_data : Path
    preprocessor_path : Path
    model_path : Path
    n_iter : int
    scoring : str
    cv : int
    target_column : str

@dataclass(frozen=True)
class ModelEvaluationConfig:
    test_data : Path
    target_column : str
    preprocessor_path : Path
    best_params_path : Path
    Adaboost : Path
    CatBoost : Path
    DscisionTree : Path
    GradientBoosting : Path
    LinearRegression : Path
    RandomForest : Path
    XGBoost : Path
    mlflow_uri :str