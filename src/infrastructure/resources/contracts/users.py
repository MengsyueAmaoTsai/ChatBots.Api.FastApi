from pydantic import BaseModel


class CreatedResponse(BaseModel):
    id: str


class CreateUserRequest(BaseModel):
    pass


class UserCreatedResponse(CreatedResponse):
    pass


class UserResponse(BaseModel):
    pass


class UserDetailsResponse(UserResponse):
    pass
