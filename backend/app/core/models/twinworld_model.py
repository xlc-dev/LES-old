from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator


if TYPE_CHECKING:
    from app.core.models.household_model import Household


class TwinWorldBase(SQLModel):
    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False, min_length=1, max_length=500)

    @field_validator("description")
    @classmethod
    def ensure_description(cls, v: str):
        if v:
            if len(v) < 1 or len(v) > 500:
                raise ValueError(
                    "description must be between 1 and 300 characters"
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
