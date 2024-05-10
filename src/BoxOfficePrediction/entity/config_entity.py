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
