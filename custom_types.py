from typing import Annotated
from pydantic import EmailStr, Field, AfterValidator

from validators import pwd_validator


UserName = Annotated[str, Field(max_length=20, description="user's name")]
UserEmail = Annotated[EmailStr, Field(description="user's email")]
UserPassword = Annotated[str, Field(min_length=8), AfterValidator(pwd_validator)]

PositiveInt = Annotated[int, Field(ge=1, description="positive integer")]
