from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.core.models.household_model import Household


class TwinWorldBase(SQLModel):
    id: int = Field(primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False)


class TwinWorld(TwinWorldBase, table=True):
    household: list["Household"] = Relationship(back_populates="twinworld")
