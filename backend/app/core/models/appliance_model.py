from typing import TYPE_CHECKING
from enum import Enum

from sqlmodel import Field, Relationship

from app.core.models.base_model import BaseModel


if TYPE_CHECKING:
    from app.core.models.twinworld_model import Household


class ApplianceType(str, Enum):
    DISHWASHER = "Dishwasher"
    WASHING_MACHINE = "Washing Machine"
    TUMBLE_DRYER = "Tumble Dryer"
    ELECTRIC_VEHICLE = "Electric Vehicle"
    STOVE = "Stove"

    def __str__(self):
        return str(self.value)


class ApplianceDays(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

    def __str__(self):
        return str(self.value)


class Appliance(BaseModel, table=True):
    "Table for storing all types of appliances"

    name: ApplianceType = Field(index=True, nullable=False)
    power: int = Field(nullable=False)
    duration: int = Field(nullable=False)
    daily_usage: int = Field(nullable=False)

    household: "Household" = Relationship(back_populates="appliances")
    household_id: int = Field(foreign_key="household.id")

    appliance_windows: list["ApplianceTimeWindow"] = Relationship(
        back_populates="appliance"
    )


class ApplianceTimeWindow(BaseModel, table=True):
    day: ApplianceDays = Field(nullable=False)
    bitmap_window: int = Field(nullable=False)

    appliance: "Appliance" = Relationship(back_populates="appliance_windows")
    appliance_id: int = Field(foreign_key="appliance.id")
