# -*- coding: utf-8 -*-
"""
    This is a DTO move messages.
"""

import logging
from faker import Faker
from pydantic import BaseModel, Field
from .tool_settings import Settings

fk = Faker()
_set = Settings()
log = logging.getLogger(_set.environment)


class EventTransport(BaseModel):
    """
        This class is the message we get from AMQP
    """
    resource: str = Field(default=_set.db_name)
    operation: str = Field(default="GET", examples=["POST", "PUT", "DELETE"])
    origen: str
    body: str | None = Field(default=None)
