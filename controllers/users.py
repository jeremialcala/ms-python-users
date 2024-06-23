# -*- coding: utf-8 -*-
"""
    This controller handles the user data lifecycle.

"""
import logging
import logging.config
import json
from inspect import currentframe
from functools import wraps

import mongoengine.errors

from classes import Settings, User
from constants import STARTING_AT, ENDING_AT
from utils import configure_logging

_set = Settings()
log = logging.getLogger(__name__)
logging.config.dictConfig(configure_logging())


def user_lifecycle(func):
    """

    :return: Response code with the result of this operation
    """
    log.info(STARTING_AT, currentframe().f_code.co_name)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
            This is a Wrapper is used to execute the lifecycle operations.
            With this tool we are going to make templates out of this code.

            TODO: Create the security module to deserialize a JWE message
            TODO: Separate all operation on different methods and use match to execute here
        :return:
        """
        log.info(STARTING_AT, currentframe().f_code.co_name)
        body = json.loads(bytes.decode(kwargs.get("body"), "UTF-8"))

        try:
            user = User.from_json(json.dumps(body))
            user.save()
            log.info(user.to_json())
        except mongoengine.errors.OperationError as e:
            log.error(e.args[-1])

        log.info(ENDING_AT, currentframe().f_code.co_name)
        return func(*args, **kwargs)

    log.info(ENDING_AT, currentframe().f_code.co_name)
    return wrapper
