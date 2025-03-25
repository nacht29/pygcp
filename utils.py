import os
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

def get_month_year(month_name:bool):
	if month_name:
		month = calendar.month_name[datetime.now().month]
	else:
		month = datetime.now().month
	year = datetime.now().year

	return (month, year)

def gen_file_name(prefix:str, infile_name:str, infile_type:str, outfile_type:str, suffix:str):
	file_name = f"{prefix}{infile_name.replace(infile_type,'')}{suffix}"
	return file_name

def snake_case(col: str) -> str:
	return col.lower().strip().replace(' ', '_').replace('-', '_')