"""This file contains the model for the Twinworld table.

The Twinworld table is used to store all the Twinworlds that are available
to use in the simulation. The twinworlds contain the households, which contain
the appliances which will be planned in using the algorithm.
"""

from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator


if TYPE_CHECKING:
    from app.core.models.household_model import Household


class TwinWorldBase(SQLModel):
    "Twinworld model that saves the twinworlds in the database"

    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False, min_length=1, max_length=500)

    @field_validator("description")
    @classmethod
    def ensure_description(cls, v: str):
        if v:
            if len(v) < 1 or len(v) > 500:
                raise ValueError(
                    "description must be between 1 and 500 characters"
                )
            return v


class TwinWorld(TwinWorldBase, table=True):
    id: int = Field(primary_key=True)

    household: list["Household"] = Relationship(
        back_populates="twinworld",
        sa_relationship_kwargs={"cascade": "delete"},
    )


class TwinWorldRead(TwinWorldBase):
    id: int


class TwinWorldCreate(TwinWorldBase):
    pass


class TwinWorldUpdate(TwinWorldBase):
    pass
