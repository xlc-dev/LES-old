from sqlmodel import Session, select

from app.core.crud.base import CRUDBase
from app.core.models.algorithm_model import (
    Algorithm,
    AlgorithmCreate,
    AlgorithmUpdate,
)


class CRUDAlgorithm(CRUDBase[Algorithm, AlgorithmCreate, AlgorithmUpdate]):
    def get_by_name(self, *, session: Session, name: str):
        "Get a single Algorithm by name"

        return session.exec(
            select(Algorithm).where(Algorithm.name == name)
        ).first()


algorithm_crud = CRUDAlgorithm(Algorithm)
