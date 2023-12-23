from typing import TYPE_CHECKING, Optional, Any
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator


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

    appliance_time_daily: list["ApplianceTimeDaily"] = Relationship(
        back_populates="appliance"
    )

    appliance_time_no_energy_daily: list[
        "ApplianceTimeNoEnergyDaily"
    ] = Relationship(back_populates="appliance")


class ApplianceTimeWindowBase(SQLModel):
    day: ApplianceDays = Field(
        nullable=False
    )  # day of week, example = "Monday"
    bitmap_window: int = Field(nullable=False)  # 24 bit bitmap


class ApplianceTimeWindow(ApplianceTimeWindowBase, table=True):
    id: int = Field(
        primary_key=True
    )  # id number of the appliance whose availability is created, example=0

    appliance: "Appliance" = Relationship(back_populates="appliance_windows")
    appliance_id: int = Field(foreign_key="appliance.id")


class ApplianceTimeDailyBase(SQLModel):
    day: int = Field(
        nullable=False, ge=1
    )  # Number day of reviewed dataset, example=1
    bitmap_plan: Optional[int] = Field(nullable=True)  # 24 bit bitmap

    @field_validator("bitmap_plan")
    @classmethod
    def ensure_bitmap_plan(cls, v: Any):
        if v:
            if v < 0 and v > 2**24 - 1:
                raise ValueError("Bit length unequal to 24")
            return v


class ApplianceTimeDaily(ApplianceTimeDailyBase, table=True):
    id: int = Field(
        primary_key=True
    )  # id number of the appliance that is being planned in, example=0

    appliance: "Appliance" = Relationship(
        back_populates="appliance_time_daily"
    )
    appliance_id: int = Field(foreign_key="appliance.id")


class ApplianceTimeNoEnergyDailyBase(SQLModel):
    day: int = Field(
        nullable=False, ge=1
    )  # Number day of reviewed dataset, example=1
    bitmap_plan: Optional[int] = Field(nullable=True)  # 24 bit bitmap

    @field_validator("bitmap_plan")
    @classmethod
    def ensure_bitmap_plan(cls, v: Any):
        if v:
            if v < 0 and v > 2**24 - 1:
                raise ValueError("Bit length unequal to 24")
            return v


class ApplianceTimeNoEnergyDaily(ApplianceTimeNoEnergyDailyBase, table=True):
    id: int = Field(
        primary_key=True
    )  # id number of the appliance that is being planned in, example=0

    appliance: "Appliance" = Relationship(
        back_populates="appliance_time_no_energy_daily"
    )
    appliance_id: int = Field(foreign_key="appliance.id")


class ApplianceTimeDailyRead(ApplianceTimeDailyBase):
    pass


class ApplianceTimeDailyCreate(ApplianceTimeDailyBase):
    pass


class ApplianceTimeDailyUpdate(ApplianceTimeDailyBase):
    pass


class ApplianceTimeNoEnergyDailyRead(ApplianceTimeNoEnergyDailyBase):
    pass


class ApplianceTimeNoEnergyDailyCreate(ApplianceTimeNoEnergyDailyBase):
    pass


class ApplianceTimeNoEnergyDailyUpdate(ApplianceTimeNoEnergyDailyBase):
    pass


class ApplianceTimeWindowRead(ApplianceTimeWindowBase):
    pass


class ApplianceTimeWindowCreate(ApplianceTimeWindowBase):
    pass


class ApplianceTimeWindowUpdate(ApplianceTimeWindowBase):
    pass


class ApplianceRead(ApplianceBase):
    id: int
    appliance_windows: list[ApplianceTimeWindowRead] = []


class ApplianceCreate(ApplianceBase):
    pass


class ApplianceUpdate(ApplianceBase):
    pass
