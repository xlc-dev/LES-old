from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.core.models.appliance_model import Appliance
    from app.core.models.twinworld_model import TwinWorld


class Household(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    size: int = Field(default=1, nullable=False)
    energy_usage: int = Field(nullable=False)
    solar_panels: int = Field(default=0, nullable=False)
    solar_yield_yearly: int

    twinworld_id: int = Field(foreign_key="twinworld.id")
    twinworld: "TwinWorld" = Relationship(back_populates="household")

    appliances: list["Appliance"] = Relationship(back_populates="household")
