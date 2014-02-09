"""
NIQuery App
"""
__author__ = 'Nolan Nichols <nolan.nichols@gmail.com>'

from __future__ import unicode_literals

import os
import logging
import argparse

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import json as json_flask
from flask.wrappers import Request, _missing, _get_data
