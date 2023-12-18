from typing import TYPE_CHECKING, Optional
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship


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


class ApplianceBase(SQLModel):
    name: ApplianceType = Field(index=True, nullable=False)
    power: float = Field(nullable=False)  # in Kwh
    duration: int = Field(nullable=False)  # in hours
    daily_usage: float = Field(nullable=False)  # in hours


class Appliance(ApplianceBase, table=True):
    id: int = Field(primary_key=True)

    household: "Household" = Relationship(back_populates="appliances")
    household_id: int = Field(foreign_key="household.id")

    appliance_windows: list["ApplianceTimeWindow"] = Relationship(
        back_populates="appliance"
    )


class ApplianceTimeWindowBase(SQLModel):
    day: ApplianceDays = Field(nullable=False)
    bitmap_window: int = Field(nullable=False)  # 24 bit bitmap
    bitmap_plan: Optional[int] = Field(nullable=True)  # 24 bit bitmap


class ApplianceTimeWindow(ApplianceTimeWindowBase, table=True):
    id: int = Field(primary_key=True)

    appliance: "Appliance" = Relationship(back_populates="appliance_windows")
    appliance_id: int = Field(foreign_key="appliance.id")


class ApplianceTimeWindowRead(ApplianceTimeWindowBase):
    pass


class ApplianceTimeWindowCreate(ApplianceTimeWindowBase):
    pass


class ApplianceTimeWindowUpdate(ApplianceTimeWindowBase):
    pass


class ApplianceRead(ApplianceBase):
    appliance_windows: list[ApplianceTimeWindowRead] = []


class ApplianceCreate(ApplianceBase):
    pass


class ApplianceUpdate(ApplianceBase):
    pass
