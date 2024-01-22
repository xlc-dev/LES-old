from typing import TYPE_CHECKING, Sized

from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator

from app.core.models.appliance_model import ApplianceRead

if TYPE_CHECKING:
    from app.core.models.appliance_model import Appliance
    from app.core.models.twinworld_model import TwinWorld


class HouseholdBase(SQLModel):
    name: str = Field(
        index=True, unique=True, nullable=False, min_length=1, max_length=15
    )
    size: int = Field(default=1, nullable=False, ge=1, le=5)
    energy_usage: int = Field(nullable=False, ge=0)
    solar_panels: int = Field(default=0, nullable=False, ge=0)
    solar_yield_yearly: int

    @field_validator("name")
    @classmethod
    def ensure_name(cls, v: Sized):
        if v:
            if not (1 <= len(v) <= 15):
                raise ValueError("name must be between 1 and 15 characters")
            return v

    @field_validator("size")
    @classmethod
    def ensure_size(cls, v: int):
        if v:
            if v < 1 or v > 5:
                raise ValueError("size must be between 1 and 5")
            return v


class Household(HouseholdBase, table=True):
    id: int = Field(primary_key=True)

    twinworld_id: int = Field(foreign_key="twinworld.id", ge=1)
    twinworld: "TwinWorld" = Relationship(back_populates="household")

    household_energy_usage: list["HouseholdEnergyUsage"] = Relationship(
        back_populates="household"
    )

    appliances: list["Appliance"] = Relationship(
        back_populates="household",
        sa_relationship_kwargs={"cascade": "delete"},
    )


class HouseholdEnergyUsageBase(SQLModel):
    day: int = Field(nullable=True)
    energyusage: float = Field(nullable=True)


class HouseholdEnergyUsage(HouseholdEnergyUsageBase, table=True):
    id: int = Field(
        primary_key=True
    )  # id number of the appliance that is being planned in, example=0

    household: "Household" = Relationship(
        back_populates="household_energy_usage"
    )
    household_id: int = Field(foreign_key="household.id")


class HouseholdRead(HouseholdBase):
    id: int
    appliances: list[ApplianceRead] = []
    twinworld_id: int


class HouseholdCreate(HouseholdBase):
    twinworld_id: int

    @field_validator("twinworld_id")
    @classmethod
    def ensure_twinworld_id(cls, v: int):
        if v:
            if v < 1:
                raise ValueError("twinworld_id must be greater than 0")
            return v


class HouseholdUpdate(HouseholdBase):
    pass


class HouseholdEnergyUsageRead(HouseholdBase):
    pass


class HouseholdEnergyUsageCreate(HouseholdBase):
    pass


class HouseholdEnergyUsageUpdate(HouseholdBase):
    pass
