from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from app.core.models.appliance_model import ApplianceRead

if TYPE_CHECKING:
    from app.core.models.appliance_model import Appliance
    from app.core.models.twinworld_model import TwinWorld


class HouseholdBase(SQLModel):
    name: str = Field(index=True, unique=True, nullable=False)
    size: int = Field(default=1, nullable=False)
    energy_usage: int = Field(nullable=False)
    solar_panels: int = Field(default=0, nullable=False)
    solar_yield_yearly: int


class Household(HouseholdBase, table=True):
    id: int = Field(primary_key=True)

    twinworld_id: int = Field(foreign_key="twinworld.id")
    twinworld: "TwinWorld" = Relationship(back_populates="household")

    appliances: list["Appliance"] = Relationship(back_populates="household")
    household_energy_usage: list["HouseholdEnergyUsage"] = Relationship(
        back_populates="household"
    )
    household_energy_available: list[
        "HouseholdEnergyAvailable"
    ] = Relationship(back_populates="household")


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


class HouseholdEnergyAvailableBase(SQLModel):
    hour: int = Field(nullable=True)
    energyavailable: float = Field(nullable=True)


class HouseholdEnergyAvailable(HouseholdEnergyUsageBase, table=True):
    id: int = Field(
        primary_key=True
    )  # id number of the appliance that is being planned in, example=0

    household: "Household" = Relationship(
        back_populates="household_energy_available"
    )
    household_id: int = Field(foreign_key="household.id")


class HouseholdRead(HouseholdBase):
    id: int
    appliances: list[ApplianceRead] = []


class HouseholdCreate(HouseholdBase):
    pass


class HouseholdUpdate(HouseholdBase):
    pass


class HouseholdEnergyUsageRead(HouseholdBase):
    pass


class HouseholdEnergyUsageCreate(HouseholdBase):
    pass


class HouseholdEnergyUsageUpdate(HouseholdBase):
    pass


class HouseholdEnergyAvailableRead(HouseholdBase):
    pass


class HouseholdEnergyAvailableCreate(HouseholdBase):
    pass


class HouseholdEnergyAvailableUpdate(HouseholdBase):
    pass
