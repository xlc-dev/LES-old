from typing import Any, Generic, Optional, Type, TypeVar, Sequence

from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.models import base_model

ModelType = TypeVar("ModelType", bound=base_model.BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """CRUD object with default methods to Create, Read, Update, Delete

        :param ModelType:
            A SQLModel class
        :param CreateSchemaType:
            A Pydantic schema class for creating objects
        :param UpdateSchemaType:
            A Pydantic schema class for updating objects
        """
        self.model = model

    def get(self, *, session: Session, id: Any) -> Optional[ModelType]:
        return session.get(self.model, id)

    def get_multi(
        self, *, session: Session, skip: int = 0, limit: int = 5000
    ) -> Sequence[ModelType]:
        return session.exec(select(self.model).offset(skip).limit(limit)).all()

    def create(self, *, session: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj

    def update(
        self,
        *,
        session: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj

    def remove(self, *, session: Session, id: int) -> None:
        obj = session.get(self.model, id)

        session.delete(obj)
        session.commit()
