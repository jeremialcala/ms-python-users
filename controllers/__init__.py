"""
    This module handles the AMQP protocol, and the entities this service.
"""
from .messages import process_messages
from .amqp import (publish_message, send_message_to_queue, ack_message,
                   execute_operation, on_message, get_amqp_connection_parameters)
