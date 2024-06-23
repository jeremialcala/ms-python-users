"""
    This class test controllers/amqp.py
"""
from unittest.mock import patch, MagicMock
import pytest

import pika
from controllers import (publish_message, send_message_to_queue, ack_message,
                         execute_operation)
from classes import Settings

_set = Settings()


@pytest.fixture(name="connection_parameters")
def fixture_connection_parameters():
    """
        this is a mock connection for AMQP tests
    :return:
    """
    return pika.ConnectionParameters("localhost")


def test_get_amqp_connection_parameters():
    """
        Testing the connection parameters methods
    :return:
    """

    with patch("pika.BlockingConnection") as mock_connection:
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel


def test_execute_operation():
    """

    :return:
    """
    with patch("pika.BlockingConnection") as mock_connection:
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        execute_operation(mock_connection, mock_channel, 0, "test_message")


def test_ack_message():
    """

    :return:
    """
    with patch("pika.BlockingConnection") as mock_connection:
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        ack_message(mock_channel, 0)


def test_send_message_to_queue(connection_parameters):
    """

    :param connection_parameters:
    :return:
    """
    with patch("pika.BlockingConnection") as mock_connection:
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel

        send_message_to_queue("test_queue", _set.amqp_routing_key,
                              "test_message", connection_parameters)

        mock_connection.assert_called_once_with(connection_parameters)
        mock_channel.queue_declare.assert_called_once_with(queue="test_queue")
        mock_channel.basic_publish.assert_called_once_with(
            exchange=_set.amqp_exchange,
            routing_key=_set.amqp_routing_key,
            body="test_message",
        )


def test_publish_message(connection_parameters):
    """

    :param connection_parameters:
    :return:
    """
    with patch("pika.BlockingConnection") as mock_connection:
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel

        publish_message('test_queue', "test_message", connection_parameters)

        mock_connection.assert_called_once_with(connection_parameters)
        mock_channel.queue_declare.assert_called_once_with(queue="test_queue", durable=True)
        mock_channel.basic_publish.assert_called_once_with(
            exchange=_set.amqp_exchange,
            routing_key=_set.amqp_routing_key,
            body="test_message",
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
