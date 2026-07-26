from app.generator.extractors.electrical_ratings import extract_ratings
from app.models.cell_data import DatasheetMetrics

def parse_datasheet(pdf_path: str) -> DatasheetMetrics:
    data = extract_ratings(pdf_path)
    return DatasheetMetrics(**data)
