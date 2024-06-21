# -*- coding: utf-8 -*-
"""
    This controller will receive, process and send messages with the process result.

"""
import logging.config

import functools
from inspect import currentframe
import keyboard

from classes import Settings
from utils import configure_logging

from .amqp import get_amqp_connection, on_message
_set = Settings()

log = logging.getLogger(__name__)
logging.config.dictConfig(configure_logging())


def process_messages(queue=_set.queue_name, _conn=get_amqp_connection()):
    """
        This method will open a queue and send using the AMQP controller to be processed
    :param queue:
    :param _conn:
    :return:
    """
    log.info("Starting: %s", currentframe().f_code.co_name)
    while True:
        channel = _conn.channel()
        channel.queue_declare(queue=queue, auto_delete=False)
        channel.queue_bind(queue=queue,
                           exchange=_set.amqp_exchange,
                           routing_key=_set.amqp_routing_key)
        threads = []
        channel.basic_qos(prefetch_count=1)
        on_message_callback = functools.partial(on_message, args=(_conn, threads))
        channel.basic_consume(queue=queue, on_message_callback=on_message_callback)
        channel.start_consuming()

        for thread in threads:
            thread.join()

        if keyboard.is_pressed('q'):
            channel.stop_consuming()
            break

    log.info("Ending: %s", currentframe().f_code.co_name)
