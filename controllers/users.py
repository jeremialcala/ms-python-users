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

from classes import Settings, User, EventTransport
from constants import STARTING_AT, ENDING_AT
from enums import ResponseCodes
from utils import configure_logging
python
_set = Settings()
log = logging.getLogger(__name__)
logging.config.dictConfig(configure_logging())


def user_lifecycle(func):
    """
        This is a function that process messages outside the AMQP controller.
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
        event = EventTransport(**json.loads(bytes.decode(args[3], "UTF-8")))
        log.info(event.body)

        log.info(ENDING_AT, currentframe().f_code.co_name)
        return func(*args, **kwargs)

    log.info(ENDING_AT, currentframe().f_code.co_name)
    return wrapper


def ctr_new_user(body: dict):
    """
    :param body:
    :return:
    """
    log.info(STARTING_AT, currentframe().f_code.co_name)
    resp = {"code": ResponseCodes.ERR, "msg": "There is an error on this process"}
    try:
        user = User.from_json(json.dumps(body))
        user.save()
        resp = {"code": ResponseCodes.AOK, "msg": "This process completed OK"}
    except mongoengine.errors.OperationError as e:
        log.error(e.args[-1])
        resp = {"code": ResponseCodes.ERR, "msg": e.args[-1]}
    finally:
        log.info(ENDING_AT, currentframe().f_code.co_name)

    return resp
