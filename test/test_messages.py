"""
    This class test controllers/messages.py
"""
from unittest.mock import patch, MagicMock

import pytest
import pika

from controllers import process_messages
from classes import Settings

_set = Settings()


@pytest.fixture(name="connection_parameters")
def fixture_connection_parameters():
    """
        this is a mock connection for AMQP tests
    :return:
    """
    return pika.ConnectionParameters("localhost")


def test_process_messages(connection_parameters):
    """

    :param connection_parameters:
    :return:
    """
    with patch("pika.BlockingConnection") as mock_connection:
        mock_channel = MagicMock()
        mock_channel.queue_bind()
        mock_connection.return_value.channel.return_value = mock_channel

        process_messages("users", connection_parameters)

        mock_connection.assert_called_once_with(connection_parameters)
        mock_channel.queue_declare.assert_called_once_with(queue="users",
                                                           auto_delete=False)

        mock_channel.start_consuming.assert_called_once()
