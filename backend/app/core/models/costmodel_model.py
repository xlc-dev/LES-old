"""This file contains the model for the Costmodel table.

The CostModel table is used to store all the CostModels that are available
to use in the simulation. The CostModels are used to find the prices for
buying and selling energy at a given date.
"""

from typing import Optional

from sqlmodel import SQLModel, Field

from pydantic import field_validator


class CostModelBase(SQLModel):
    """Costmodel model that saves the costmodel in the database.

    price_network_buy_consumer and price_network_sell_consumer are respectively
    the price for buying and selling from the outside energy provider.
    fixed_price_ratio is the ratio between these for determining the price if
    the fixed price option is selected as the costmodel.
    """

    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False, min_length=1, max_length=500)
    price_network_buy_consumer: float = Field(
        nullable=False
    )  # in local currency
    price_network_sell_consumer: float = Field(
        nullable=False
    )  # in local currency
    fixed_price_ratio: Optional[float] = Field(
        nullable=True
    )  # a fraction between 0 and 1
    algorithm: str = Field(nullable=False)

    @field_validator("description")
    @classmethod
    def ensure_description(cls, v: str):
        if v:
            if len(v) < 1 or len(v) > 500:
                raise ValueError(
                    "description must be between 1 and 500 characters"
                )
            return v


class CostModel(CostModelBase, table=True):
    id: int = Field(primary_key=True)


class CostModelRead(CostModelBase):
    id: int


class CostModelCreate(CostModelBase):
    pass


class CostModelUpdate(CostModelBase):
    pass
