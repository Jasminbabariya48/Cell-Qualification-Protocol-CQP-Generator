from pydantic import BaseModel
from typing import List

class TestParameter(BaseModel):
    sr_no: int
    parameter: str
    acceptance_limit: str
    clause: str

class DutyProfile(BaseModel):
    name: str
    rates: List[str]
    tests: List[TestParameter]
