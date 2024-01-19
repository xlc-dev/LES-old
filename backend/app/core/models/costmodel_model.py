"""This file contains the model for the Algorithm table.

The CostModel table is used to store all the CostModels that are available
to use in the simulation. The CostModels are used to find the best....
"""

from typing import Optional

from sqlmodel import SQLModel, Field


class CostModelBase(SQLModel):
    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False)
    price_network_buy_consumer: float = Field(nullable=False)
    price_network_sell_consumer: float = Field(nullable=False)
    fixed_price_ratio: Optional[float] = Field(nullable=True)
    algorithm: str = Field(nullable=False)


class CostModel(CostModelBase, table=True):
    id: int = Field(primary_key=True)


class CostModelRead(CostModelBase):
    id: int


class CostModelCreate(CostModelBase):
    pass


class CostModelUpdate(CostModelBase):
    pass
