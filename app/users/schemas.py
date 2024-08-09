from pydantic import BaseModel

class User(BaseModel):
    name: str
    second_name: str

class UserCreate(User):
    pass

class UserResponse(User):
    id: int

    class Config:
        model_config = {'from_attributes': True}