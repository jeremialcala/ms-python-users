# -*- coding: utf-8 -*-
"""
    This controller manages the AMQP, serving as the RabbitMQ interface.

"""
import threading
import logging.config
import functools

from inspect import currentframe
import pika
from pika.channel import Channel

from classes import Settings
from utils import configure_logging
from constants import STARTING_AT, ENDING_AT


_set = Settings()
log = logging.getLogger(__name__)
logging.config.dictConfig(configure_logging())


def get_amqp_connection():
    """
    :return: pika Connection parameters for RabbitMQ.
    """
    log.info(STARTING_AT, currentframe().f_code.co_name)
    credentials = pika.credentials.PlainCredentials(username=_set.qms_user,
                                                    password=_set.qms_password)

    conn_parameters = pika.ConnectionParameters(host=_set.qms_server,
                                                port=_set.qms_port,
                                                credentials=credentials)
    log.info(ENDING_AT, currentframe().f_code.co_name)
    return pika.BlockingConnection(conn_parameters)


def on_message(channel: Channel, method_frame: any, header_frame: any, body: any, args: any) -> None:
    """
        This method creates an event to process AMQP messages.

    :param channel:
    :param method_frame:
    :param header_frame:
    :param body:
    :param args:
    """

    log.info(STARTING_AT, currentframe().f_code.co_name)
    log.info("Headers of this message: %s", header_frame)
    (_connection, _threads) = args
    t = threading.Thread(
        target=execute_operation, args=(_connection,
                                        channel, method_frame.delivery_tag, body))
    t.start()
    _threads.append(t)
    log.info(ENDING_AT, currentframe().f_code.co_name)


def execute_operation(connection, channel, delivery_tag, body):
    """
        this executes work on a thread and after marks ACK the message.

    """
    log.info(STARTING_AT, currentframe().f_code.co_name)
    thread_id = threading.get_ident()
    log.info('Thread id: %s Delivery tag: %s Message body: %s',
             thread_id, delivery_tag, body)

    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)
    log.info(ENDING_AT, currentframe().f_code.co_name)


def ack_message(channel, delivery_tag) -> None:
    """
        Note that `channel` must be the same pika channel instance via which
        the message being ACKed was retrieved (AMQP protocol constraint).

    """
    log.info(STARTING_AT, currentframe().f_code.co_name)
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass
    log.info(ENDING_AT, currentframe().f_code.co_name)


def send_message_to_queue(queue: str, routing_key: str, message, connection) -> None:
    """
        this will send a Message to a queue

    """
    log.info(STARTING_AT, currentframe().f_code.co_name)

    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange=_set.amqp_exchange,
                          routing_key=routing_key,
                          body=message.encode("utf-8"))
    connection.close()
    log.info(ENDING_AT, currentframe().f_code.co_name)


def publish_message(queue, message, connection_parameters):
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange=_set.amqp_exchange,
        routing_key=_set.amqp_routing_key,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )
    connection.close()
