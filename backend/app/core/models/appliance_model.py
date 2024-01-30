"""This file contains the model for the Appliance table.

The Appliance table is used to store all the appliance that are present
in a household. The appliances are planned in by the algorithms.
"""

from typing import TYPE_CHECKING, Any
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator


if TYPE_CHECKING:
    from app.core.models.twinworld_model import Household


class ApplianceType(str, Enum):
    "Contains all the appliances available in the default twinworld"

    DISHWASHER = "Dishwasher"
    WASHING_MACHINE = "Washing Machine"
    TUMBLE_DRYER = "Tumble Dryer"
    ELECTRIC_VEHICLE = "Electric Vehicle"
    STOVE = "Stove"

    def __str__(self):
        return str(self.value)


class ApplianceDays(str, Enum):
    "Contains the days of the week as variable"

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
    "Appliance model that saves the appliances in the database"
    name: ApplianceType = Field(index=True, nullable=False)
    power: float = Field(nullable=False, gt=0)  # in Kwh
    duration: int = Field(nullable=False, gt=0)  # in hours
    daily_usage: float = Field(
        nullable=False, gt=0
    )  # in amount of times used per day

    @field_validator("power")
    @classmethod
    def ensure_power(cls, v: Any):
        if v:
            if v < 0:
                raise ValueError("power must be greater than 0")
            return v

    @field_validator("duration")
    @classmethod
    def ensure_duration(cls, v: Any):
        if v:
            if v < 0:
                raise ValueError("duration must be greater than 0")
            return v

    @field_validator("daily_usage")
    @classmethod
    def ensure_daily_usage(cls, v: Any):
        if v:
            if v < 0:
                raise ValueError("daily_usage must be greater than 0")
            return v


class Appliance(ApplianceBase, table=True):
    "Contains all the appliances that are present in a household"

    id: int = Field(primary_key=True)

    household: "Household" = Relationship(back_populates="appliances")
    household_id: int = Field(foreign_key="household.id")

    appliance_windows: list["ApplianceTimeWindow"] = Relationship(
        back_populates="appliance",
        sa_relationship_kwargs={"cascade": "delete"},
    )

    appliance_time_daily: list["ApplianceTimeDaily"] = Relationship(
        back_populates="appliance"
    )


class ApplianceTimeWindowBase(SQLModel):
    """When an appliance can be planned in.

    The bitmap window contains 24 possible hours"""

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
    """When an appliance is planned in.

    Different from the window. The bitmaps contain 24 possible hours
    """

    day: int = Field(
        nullable=False, ge=1
    )  # Number day of reviewed dataset, example=1
    bitmap_plan_energy: int = Field(
        default=0, nullable=False, ge=0, le=2**24 - 1
    )
    bitmap_plan_no_energy: int = Field(
        default=0, nullable=False, ge=0, le=2**24 - 1
    )

    @field_validator("bitmap_plan_energy")
    @classmethod
    def ensure_bitmap_plan_energy(cls, v: Any):
        if v:
            if v < 0 and v > 2**24 - 1:
                raise ValueError("Bit length unequal to 24")
            return v
        # If value is None, just set to 0
        else:
            return 0

    @field_validator("bitmap_plan_no_energy")
    @classmethod
    def ensure_bitmap_plan_no_energy(cls, v: Any):
        if v:
            if v < 0 and v > 2**24 - 1:
                raise ValueError("Bit length unequal to 24")
            return v
        # If value is None, just set to 0
        else:
            return 0


class ApplianceTimeDaily(ApplianceTimeDailyBase, table=True):
    id: int = Field(
        primary_key=True
    )  # id number of the appliance that is being planned in, example=0

    appliance: "Appliance" = Relationship(
        back_populates="appliance_time_daily"
    )
    appliance_id: int = Field(foreign_key="appliance.id")


class ApplianceTimeDailyRead(ApplianceTimeDailyBase):
    id: int


class ApplianceTimeDailyCreate(ApplianceTimeDailyBase):
    pass


class ApplianceTimeDailyUpdate(ApplianceTimeDailyBase):
    pass


class ApplianceTimeWindowRead(ApplianceTimeWindowBase):
    id: int


class ApplianceTimeWindowCreate(ApplianceTimeWindowBase):
    appliance_id: int


class ApplianceTimeWindowUpdate(ApplianceTimeWindowBase):
    pass


class ApplianceRead(ApplianceBase):
    id: int
    appliance_windows: list[ApplianceTimeWindowRead] = []


class ApplianceCreate(ApplianceBase):
    household_id: int

    @field_validator("household_id")
    @classmethod
    def ensure_household_id(cls, v: Any):
        if v:
            if v < 1:
                raise ValueError("household_id must be greater than 0")
            return v


class ApplianceUpdate(ApplianceBase):
    pass
