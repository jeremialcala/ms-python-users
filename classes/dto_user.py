# -*- coding: utf-8 -*-
"""
    This DTO transfer data to the user entity
"""
from faker import Faker
from pydantic import BaseModel, Field

fk = Faker()


class Users(BaseModel):
    """
        Class users is a DTO for transforming the message body to create a user entity

    """
    firstName: str = Field(default=fk.first_name())
    middleName: str | None = Field(default=fk.first_name())
    lastName: str = Field(default=fk.last_name())
    emailAddress: str = Field(default=fk.email(domain="gmail.com"))
    phoneNumber: str = Field(default=fk.phone_number())
