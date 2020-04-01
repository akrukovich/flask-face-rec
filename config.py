# -*- coding: utf-8 -*-
"""
Configuration module.

This module contains configuration class which used for app creation.
"""
import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """
    Configuration class.

    Class with environmental variables for app instance.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SecretKey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://' \
                                                                'postgres:' \
                                                                '12345678' \
                                                                '@localhost:' \
                                                                '5432/facedb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = 0
