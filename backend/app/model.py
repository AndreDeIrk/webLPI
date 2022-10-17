from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    fullname: int = Field(default=None)
    telegram: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "telegram": "and1661",
                "password": "weakpassword",
            }
        }


class UserLoginSchema(BaseModel):
    telegram: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "telegram": "and1661",
                "password": "weakpassword",
            }
        }