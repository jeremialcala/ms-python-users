# -*- coding: utf-8 -*-
"""
    This controller manages the AMQP, serving as the RabbitMQ interface.

"""

import base64
import json

import threading
import logging.config
import functools
from uuid import UUID, uuid4
import asyncio
from datetime import datetime
from asyncio import ensure_future
from inspect import currentframe
import pika

from classes import Settings
from utils import configure_logging

_set = Settings()
log = logging.getLogger(__name__)
logging.config.dictConfig(configure_logging())


def get_amqp_connection():
    """
    :return: pika Connection parameters for RabbitMQ.
    """
    log.info("Starting: %s", currentframe().f_code.co_name)

    credentials = pika.credentials.PlainCredentials(username=_set.qms_user,
                                                    password=_set.qms_password)

    conn_parameters = pika.ConnectionParameters(host=_set.qms_server,
                                                port=_set.qms_port,
                                                credentials=credentials)

    log.info("Ending: %s", currentframe().f_code.co_name)
    return pika.BlockingConnection(conn_parameters)


def on_message(_channel, method_frame, header_frame, body, args):
    """
        This method creates an event to process AMQP messages.

    :param _channel:
    :param method_frame:
    :param header_frame:
    :param body:
    :param args:
    :return:
    """
    log.info("Starting: %s", currentframe().f_code.co_name)
    log.info("Headers of this message: %s", header_frame)
    (_connection, _threads) = args
    t = threading.Thread(
        target=do_work, args=(_connection,
                              _channel, method_frame.delivery_tag, body))
    t.start()
    _threads.append(t)
    log.info("Ending: %s", currentframe().f_code.co_name)


def do_work(connection, channel, delivery_tag, body):
    """
        this executes work on a thread and after marks ACK the message.

    :param connection:
    :param channel:
    :param delivery_tag:
    :param body:
    :return:
    """
    log.info("Starting: %s", currentframe().f_code.co_name)
    thread_id = threading.get_ident()
    log.info('Thread id: %s Delivery tag: %s Message body: %s',
             thread_id, delivery_tag, body)

    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)
    log.info("Ending: %s", currentframe().f_code.co_name)


def ack_message(channel, delivery_tag):
    """
        Note that `channel` must be the same pika channel instance via which
        the message being ACKed was retrieved (AMQP protocol constraint).

    :param channel:
    :param delivery_tag:
    :return:
    """
    log.info("Starting: %s", currentframe().f_code.co_name)
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass
    log.info("Ending: %s", currentframe().f_code.co_name)


def send_message_to_queue(queue: str, routing_key:str, message):
    """
        this will send a Message to a queue

    :param queue: this is the name of the queue to send the message
    :param message:
    :param routing_key:
    :return:
    """
    log.info("Starting: %s", currentframe().f_code.co_name)
    connection = get_amqp_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange=_set.amqp_exchange,
                          routing_key=routing_key,
                          body=message.to_json().encode("utf-8"))
    connection.close()
    log.info("Ending: %s", currentframe().f_code.co_name)
