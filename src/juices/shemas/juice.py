from pydantic import BaseModel, Field


class JuiceResponse(BaseModel):
    id: int
    volume: float
    flavor: str
    price: float

    model_config = {
        "from_attributes": True
    }


class JuiceRequestCreate(BaseModel):
    volume: float = Field(..., gt=0)
    flavor: str
    price: float = Field(..., gt=0)


class JuiceRequestPriceUpdate(BaseModel):
    price: float = Field(..., gt=0)
