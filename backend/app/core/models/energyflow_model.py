"""This file contains the model for the Energyflow table.

The Energyflow table is used to store all the energy usage and the
internal yield of green energy that is available to be used in the simulation.
"""

from sqlmodel import SQLModel, Field, Relationship

from pydantic import field_validator


class EnergyFlowBase(SQLModel):
    "Energyflow model that saves the energyflow in the database"

    timestamp: int = Field(nullable=False, index=True)  # in unix
    energy_used: float = Field(nullable=False)  # in kWh
    solar_produced: float = Field(nullable=False)  # in kWh


class EnergyFlow(EnergyFlowBase, table=True):
    id: int = Field(primary_key=True)

    energyflow_upload: "EnergyFlowUpload" = Relationship(
        back_populates="energyflows"
    )
    energyflow_upload_id: int = Field(foreign_key="energyflowupload.id")


class EnergyFlowRead(EnergyFlowBase):
    pass


class EnergyFlowCreate(EnergyFlowBase):
    energyflow_upload_id: int


class EnergyFlowUpdate(EnergyFlowBase):
    pass


class EnergyFlowUploadBase(SQLModel):
    "Upload table for uploading CSV Energyflows"

    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False)

    solar_panels_factor: int = Field(
        nullable=False, ge=1
    )  # amount of solar panels that are available in the energyflow
    energy_usage_factor: int = Field(
        nullable=False, ge=1
    )  # yearly energy usage in kWh by the house in the energyflow file

    @field_validator("solar_panels_factor")
    @classmethod
    def ensure_solar_panels_factor(cls, v: int):
        if v:
            if v < 1:
                raise ValueError("solar_panels_factor must be greater than 0")
            return v

    @field_validator("energy_usage_factor")
    @classmethod
    def ensure_energy_usage_factor(cls, v: int):
        if v:
            if v < 1:
                raise ValueError("energy_usage_factor must be greater than 0")
            return v


class EnergyFlowUpload(EnergyFlowUploadBase, table=True):
    id: int = Field(primary_key=True)

    energyflows: list["EnergyFlow"] = Relationship(
        back_populates="energyflow_upload",
        sa_relationship_kwargs={"cascade": "delete"},
    )


class EnergyFlowUploadRead(EnergyFlowUploadBase):
    id: int


class EnergyFlowUploadCreate(EnergyFlowUploadBase):
    pass


class EnergyFlowUploadUpdate(EnergyFlowUploadBase):
    pass
