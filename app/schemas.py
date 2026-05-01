from pydantic import BaseModel
from datetime import datetime



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


