from typing import Annotated

from pydantic import BaseModel, Field, WithJsonSchema


class JuiceDTO(BaseModel):
    id: int
    volume: float
    flavor: str
    price: float

    class Config:
        orm_mode = True
        from_attributes = True


class PaginationRequest(BaseModel):
    page: int = Field(ge=1, default=1)
    limit: int = Field(ge=1, le=100, default=10)


class JuiceResponse(BaseModel):
    id: int
    volume: float
    flavor: str
    price: float

    model_config = {
        "from_attributes": True
    }


class JuiceRequestCreate(BaseModel):
    volume: Annotated[float, Field(gt=0, strict=True), WithJsonSchema({'extra': 'data'})]
    flavor: Annotated[str, Field(strict=True), WithJsonSchema({'extra': 'data'})]
    price: Annotated[float, Field(gt=0, strict=True), WithJsonSchema({'extra': 'data'})]


class JuiceRequestPriceUpdate(BaseModel):
    price: Annotated[float, Field(gt=0, strict=True), WithJsonSchema({'extra': 'data'})]
