import inspect
from typing import Type
import datetime
from typing import Optional, List
from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        if not model_field.required:
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(model_field.default),
                    annotation=model_field.outer_type_,
                )
            )
        else:
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(...),
                    annotation=model_field.outer_type_,
                )
            )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls


class User1(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    dob: Optional[datetime.date]
    gender: Optional[str]
    con_password: Optional[str]
    expires_in: Optional[str]
    address: Optional[str]
    about_me: Optional[str]


@as_form
class UserInDB(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    dob: Optional[datetime.date]
    gender: Optional[str]
    con_password: Optional[str]
    expires_in: Optional[str]
    address: Optional[str]
    about_me: Optional[str]
