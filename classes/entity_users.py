# -*- coding: utf-8 -*-
"""
    This is a Simple entity that manages Users lifecycle.
"""
import logging
from datetime import datetime
from uuid import uuid4
from mongoengine import (Document, StringField, UUIDField, DateTimeField,
                         IntField, EmailField, connect, OperationError)

from enums import Status, ResponseCodes
from .tool_settings import Settings

settings = Settings()
log = logging.getLogger(settings.environment)
logging.getLogger("pymongo").propagate = False

connect(
    db=settings.db_name,
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_host
)


class User(Document):
    """
        Class that define the users as a resource, for now we are having FName,
        LName, Email and PhoneNumber.
        {
            "firstName": fk.first_name(),
            "middleName":fk.first_name(),
            "lastName":fk.last_name(),
            "emailAddress":fk.email(domain="gmail.com"),
            "phoneNumber":fk.phone_number()
        }
        user["emailAddress"] = user["firstName"][0].lower() + user["lastName"].lower() + "@gmail.com"
        {'firstName': 'Timothy', 'middleName': 'Lauren', 'lastName': 'Esparza', 'emailAddress': 'tesparza@gmail.com', 'phoneNumber': '001-476-454-1226x4204'}

    """
    _uuid = UUIDField(required=True, unique=True, default=uuid4())
    firstName = StringField()
    middleName = StringField()
    lastName = StringField()
    emailAddress = EmailField(required=True, unique=True)
    phoneNumber = StringField()
    userType = StringField(required=True, default="User")
    createdAt = DateTimeField(required=True, default=datetime.now())
    status = IntField(required=True, default=Status.REG.value)
    statusDate = DateTimeField(required=True, default=datetime.now())

    @staticmethod
    def get_user_by_email(email: str):
        """
        :param email: This is the email address for the user we are getting
        :return: User information for this email, None if this user does not exist.
        """
        user = None
        try:
            user = list(User.objects(emailAddress=email))  # pylint: disable=no-member;
        except ValueError:
            log.error("The user with email %s was not found", email)

        return user

    @staticmethod
    def update_user_status(email: str, status: int):
        """
            Method that change user status by Email address.
        :param email: a register or active user's email address
        :param status: this is the status desired to update on this user.
        :return: a response code resulting of this operation.
        """
        try:
            log.info("updating user %s to this status %s", email, Status(status).name)
            User.objects(email_address=email).update_one(set__status=status)  # pylint: disable=no-member;
        except OperationError as e:
            log.error(e.args)
            return ResponseCodes.ERR
        log.info("User updated successfully!")
        return ResponseCodes.AOK
