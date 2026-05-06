from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List



class PostBase(BaseModel):
    item: str
    quantity: int
    price: int
    
class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    created_at: datetime
    #model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    item: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[int] = None



class MonthlyData(BaseModel):
    month: str
    monthly_expenditure: int

class SummaryResponse(BaseModel):
    year: int
    yearly_expenditure: int
    monthly_summary: List[MonthlyData]
    
