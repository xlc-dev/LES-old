from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.core.models.base_model import BaseModel


if TYPE_CHECKING:
    from app.core.models.household_model import Household


class TwinWorld(BaseModel, table=True):
    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False)

    household: list["Household"] = Relationship(back_populates="twinworld")
