from typing import Optional

from sqlmodel import SQLModel, Field


class CostModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False)
    price_network_buy_consumer: float = Field(nullable=False)
    price_network_sell_consumer: float = Field(nullable=False)
    fixed_division: Optional[float] = Field(nullable=True)
    stock_time_delta: Optional[int] = Field(nullable=True)
    algo_1: str = Field(nullable=False)
    algo_2: Optional[str] = Field(nullable=True)
