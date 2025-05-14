import os
import smtplib
from datetime import date, timedelta
from email.mime.text import MIMEText

import calendar
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

def get_year():
	year = datetime.now().year
	return year

def get_month(name=False):
	if name:
		month = calendar.month_name[datetime.now().month]
	else:
		month = datetime.now().month
	return month

def get_iso_weekyear(in_date:date=None, lpad:bool=False, lpad_num:int=0, backtrack:int=0):
	if not in_date:
		in_date = date.today()

	# backtrack n weeks from input date
	target_date = in_date - timedelta(week=backtrack)
	iso_week, iso_year, _ = target_date.iso_calendar()

	if lpad:
		if lpad_num >= 0:
			iso_week_str = str(iso_week).zfill(lpad)
			return iso_week_str
		else:
			raise ValueError('lpad must be an integer greater than 0')

	return (iso_week, iso_year)

def gen_file_name(prefix:str, infile_name:str, infile_type:str, outfile_type:str, suffix:str):
	file_name = infile_name.replace(infile_type, '')
	final_file_name = f"{prefix}{file_name}{suffix}{outfile_type}"
	return final_file_name

def snake_case(col: str) -> str:
	return col.lower().strip().replace(' ', '_').replace('-', '_')

def send_email(
		subject:str,
		message:str,
		smtp_server:str=None,
		smtp_port:int=None,
		sender_email:str=None,
		app_password:str=None,
		receiver_email:str=None,
		cc_emails:list=None
):

	# get email params from env if not provided
	smtp_server = smtp_server or os.getenv('SMTP_SERVER')
	smtp_port = smtp_port or int(os.getenv('SMTP_PORT', 587))
	sender_email = sender_email or os.getenv('SENDER_EMAIL')
	app_password = app_password or os.getenv('APP_PASSWORD')
	receiver_email = receiver_email or os.getenv('RECEIVER_EMAIL')

	# validate params
	if not all([smtp_server, smtp_port, sender_email, app_password, receiver_email]):
		raise ValueError('Missing email config params')

	# draft email
	msg = MIMEText(message)
	msg['Subject'] = subject
	msg['From'] = sender_email
	msg['To'] = receiver_email
	if cc_emails:
		msg['Cc'] = ', '.join(cc_emails)

	# send email
	try:
		with smtplib.SMTP(smtp_server, smtp_port) as server:
			server.starttls()
			server.login(sender_email, app_password)
			server.send_message(msg)
	except Exception as e:
		print(f"Failed to send email: {str(e)}")
		raise
