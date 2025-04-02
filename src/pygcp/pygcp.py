import os
import io
import calendar
import pandas as pd
import logging as log
from io import BytesIO
from google.cloud import storage
from google.cloud import bigquery as bq # bq client
from google.oauth2 import service_account
from googleapiclient.discovery import build # drive build service
from googleapiclient.http import MediaIoBaseUpload
from datetime import date, datetime, timezone, timedelta

class CustomError(Exception):
	def __init__(self, message, error_code=None):
		super().__init__(message)
		self.error_code = error_code

class SliceError(CustomError):
	def __init__(self, message="Invalid slice length. Must be at least 1."):
		super().__init__(message)