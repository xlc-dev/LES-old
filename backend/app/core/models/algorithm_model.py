"""This file contains the model for the Algorithm table.

The Algorithm table is used to store all the algorithms that are available
to use in the simulation. The algorithms are used to find the best....
"""

from typing import Optional

from sqlmodel import SQLModel, Field


class AlgorithmBase(SQLModel):
    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False)
    max_temperature: Optional[int] = Field(nullable=True)
    algorithm: str = Field(nullable=False)


class Algorithm(AlgorithmBase, table=True):
    id: int = Field(primary_key=True)


class AlgorithmRead(AlgorithmBase):
    id: int


class AlgorithmCreate(AlgorithmBase):
    pass


class AlgorithmUpdate(AlgorithmBase):
    pass
