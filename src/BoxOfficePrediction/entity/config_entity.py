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
    org_table_path : Path

