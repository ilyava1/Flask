import pydantic
from typing import Optional

class CreateAdv(pydantic.BaseModel):
    header: str
    description: str
    owner: str

    @pydantic.validator('header')
    def validate_header(cls, value):
        if len(value) < 8:
            raise ValueError('Header is less then 8 simbols, pls correct')
        return value

    @pydantic.validator('description')
    def validate_description(cls, value):
        if len(value) < 16:
            raise ValueError('Description is less then 16 simbols, pls correct')
        return value

    @pydantic.validator('owner')
    def validate_owner(cls, value):
        if len(value) < 3:
            raise ValueError('Owner name is less then 3 simbols, pls correct')
        return value

class PatchAdv(pydantic.BaseModel):
    header: Optional[str]
    description: Optional[str]
    owner: Optional[str]

    @pydantic.validator('header')
    def validate_header(cls, value):
        if len(value) < 8:
            raise ValueError('Header is less then 8 simbols, pls correct')
        return value

    @pydantic.validator('description')
    def validate_description(cls, value):
        if len(value) < 16:
            raise ValueError('Description is less then 16 simbols, pls correct')
        return value

    @pydantic.validator('owner')
    def validate_owner(cls, value):
        if len(value) < 3:
            raise ValueError('Owner name is less then 3 simbols, pls correct')
        return value