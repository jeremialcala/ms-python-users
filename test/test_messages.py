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
        This test the method process_messages from controllers
    """
    with patch("pika.BlockingConnection") as mock_connection:
        mock_channel = MagicMock()
        mock_channel.queue_bind()
        mock_connection.return_value.channel.return_value = mock_channel





