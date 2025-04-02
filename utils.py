import os
import sys
import smtplib
import traceback
from email.mime.text import MIMEText

import calendar
import logging as log
from datetime import datetime

def file_type_in_dir(file_dir:str, file_type:str):
	if file_dir is None:
		files_in_dir = os.listdir()
	else:
		files_in_dir = os.listdir(file_dir)

	if file_type is None:
		return files_in_dir
	else:
		return [file for file in files_in_dir if file.endswith(file_type)]

def get_month_year(month_name=False):
	if month_name:
		month = calendar.month_name[datetime.now().month]
	else:
		month = datetime.now().month
	year = datetime.now().year

	return (month, year)

def gen_file_name(prefix:str, infile_name:str, infile_type:str, outfile_type:str, suffix:str):
	file_name = infile_name.replace(infile_type, '')
	final_file_name = f"{prefix}{file_name}{suffix}.{outfile_type}"
	return final_file_name

def snake_case(col: str) -> str:
	return col.lower().strip().replace(' ', '_').replace('-', '_')

def send_email(subject:str, message:str,
			   smtp_server:str=None, 
			   smtp_port:int=None, 
			   sender_email:str=None,
			   sender_password:str=None, 
			   receiver_email:str=None):

	# get email params from env if not provided
	smtp_server = smtp_server or os.getenv('SMTP_SERVER')
	smtp_port = smtp_port or int(os.getenv('SMTP_PORT', 587))
	sender_email = sender_email or os.getenv('SENDER_EMAIL')
	sender_password = sender_password or os.getenv('SENDER_PASSWORD')
	receiver_email = receiver_email or os.getenv('RECEIVER_EMAIL')

	# validate params
	if not all([smtp_server, smtp_port, sender_email, sender_password, receiver_email]):
		raise ValueError('Missing email config params')

	# draft email
	msg = MIMEText(message)
	msg['Subject'] = subject
	msg['From'] = sender_email
	msg['To'] = receiver_email

	# send email
	try:
		with smtplib.SMTP(smtp_server, smtp_port) as server:
			server.starttls()
			server.login(sender_email, sender_password)
			server.send_message(msg)
	except Exception:
		log.info()
		raise