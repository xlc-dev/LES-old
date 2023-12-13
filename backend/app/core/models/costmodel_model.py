from sqlmodel import Field

from app.core.models.base_model import BaseModel


class CostModel(BaseModel, table=True):
    name: str = Field(index=True, unique=True, nullable=False)
    buy_price: int = Field(nullable=False)
    sell_price: int = Field(nullable=False)
