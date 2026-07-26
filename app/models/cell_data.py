from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.duty_profile import DutyProfile

class DatasheetMetrics(BaseModel):
    nominal_voltage: str
    v_max: str
    v_min: str
    rated_capacity: str
    grading_low: str
    grading_high: str
    format_from_datasheet: str
    manufacturer_from_datasheet: str
    storage_from_datasheet: str
    supplied_as_from_datasheet: str
    datasheet_title: str
    cell_model: Optional[str] = ""
    chemistry: Optional[str] = ""

class CellQualificationData(BaseModel):
    doc_number: str
    framework: str = "IESF-4400"
    lab: str = "Northgate Cell Qualification Laboratory (NCQL)"
    market: str
    cell_model: str
    
    chemistry: str
    tmp_doc_title: str
    acl_doc_title: str
    duty_profiles_str: str
    
    metrics: DatasheetMetrics
    duty_profiles: List[DutyProfile]
    
    footnotes: List[str] = Field(default_factory=list)
