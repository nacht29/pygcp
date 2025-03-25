import pandas as pd
import logging as log
from io import BytesIO
from datetime import datetime
from google.cloud import bigquery as bq
from google.oauth2 import service_account
from exceptions import SliceError

'''
BigQuery - client
'''

def bq_build_client(json_key:str):
	credentials = service_account.Credentials.from_service_account_file(json_key)
	bq_client = bq.Client(credentials=credentials, project=credentials.project_id)
	return bq_client

'''
BigQuery- Extract/Query from BQ
'''

def bq_to_df(bq_client, sql_script:str):
	with open(sql_script, 'r') as cur_script:
		log.info(f'\n\n{datetime.now()} Query: {sql_script}')
		query = ' '.join([line for line in cur_script])
		results_df = bq_client.query(query).to_dataframe()
		log.info(f'Results: {results_df.shape}')

	return (results_df)

# read 1 SQL script and query BQ
# slice the queried data into multiple ver of xlsx files
def bq_to_xlsx(bq_client, sql_script:str, slice_row:int, outfile_name:str):
	if not 0 < slice_row <= 1000000:
		raise SliceError('Invalid slice length.')

	results_df = bq_to_df(bq_client, sql_script)
	excel_buffers  = []

	# slice the results of each script
	for cur_row in range(0, len(results_df), slice_row):
		file_ver = cur_row // slice_row + 1
		subset_df = results_df.iloc[cur_row:cur_row + slice_row]
		outfile_name = outfile_name.replace('.xlsx', f'_{file_ver}.xlsx')

		log.info(f'{datetime.now()} creating xlsx binary for {outfile_name}')

		# init binary buffer for xlsx file
		cur_buffer = BytesIO()

		with pd.ExcelWriter(cur_buffer, engine='xlsxwriter') as writer:
			subset_df.to_excel(writer, index=False, header=True)
		cur_buffer.seek(0)

		# add the buffer data and file name to the main list
		excel_buffers.append((cur_buffer, outfile_name))

		log.info(f'{datetime.now()} {outfile_name} binary created')

	return excel_buffers

def bq_to_csv(bq_client, sql_script: str, slice_row: int, outfile_name: str):
	if not 0 < slice_row <= 1000000:
		raise SliceError('Invalid slice length.')

	results_df = bq_to_df(bq_client, sql_script)
	csv_buffers = []

	for cur_row in range(0, len(results_df), slice_row):
		file_ver = cur_row // slice_row + 1
		subset_df = results_df.iloc[cur_row:cur_row + slice_row]
		cur_outfile_name = outfile_name.replace('.csv', f'_{file_ver}.csv')

		log.info(f'{datetime.now()} creating CSV binary for {cur_outfile_name}')

		cur_buffer = BytesIO()
		subset_df.to_csv(cur_buffer, index=False)
		cur_buffer.seek(0)

		csv_buffers.append((cur_buffer, cur_outfile_name))

		log.info(f'{datetime.now()} {cur_outfile_name} CSV binary created')

	return csv_buffers

'''
BigQuery - Load to BQ
'''

def df_to_bq(bq_client, df, table_path:str, mode:str):
	if mode == 'a':
		write_dispos = 'WRITE_APPEND'
	elif mode == 't':
		write_dispos="WRITE_TRUNCATE"
	else:
		raise ValueError(f"{mode} is not recognised. Use 'a' for append or 't' for truncate")

	job_config = bq.LoadJobConfig(write_disposition='WRITE_TRUNCATE', autodetect=True)
	job = bq_client.load_table_from_dataframe(df, table_path, job_config=job_config)
	return job.result()

def local_csv_to_bq(bq_client, bucket_csv_path: str, project_id:str, dataset:str, table:str, mode):
	if mode == 'a':
		write_dispos = 'WRITE_APPEND'
	elif mode == 't':
		write_dispos="WRITE_TRUNCATE"
	else:
		raise ValueError(f"{mode} is not recognised. Use 'a' for append or 't' for truncate")


def bucket_csv_to_bq(bq_client, bucket_csv_path: str, project_id:str, dataset:str, table:str, mode):
	if mode == 'a':
		write_dispos = 'WRITE_APPEND'
	elif mode == 't':
		write_dispos="WRITE_TRUNCATE"
	else:
		raise ValueError(f"{mode} is not recognised. Use 'a' for append or 't' for truncate")
	
	job_config = bq.LoadJobConfig(
		source_format=bq.SourceFormat.CSV,
		skip_leading_rows=1,
		autodetect=True,
		write_disposition=write_dispos
	)

	uri = f'gs://{bucket_csv_path}/csv name'
	job = bq_client.load_table_from_uri(uri, f"{project_id}.{dataset}.{table}", job_config=job_config)
	job.result()

def gdrive_csv_to_bq(bq_client, drive_csv_path: str, project_id:str, dataset:str, table:str, mode):
	if mode == 'a':
		write_dispos = 'WRITE_APPEND'
	elif mode == 't':
		write_dispos="WRITE_TRUNCATE"
	else:
		raise ValueError(f"{mode} is not recognised. Use 'a' for append or 't' for truncate")

	job_config = bq.LoadJobConfig(
		source_format=bq.SourceFormat.CSV,
		skip_leading_rows=1,
		autodetect=True,
		write_disposition=write_dispos
	)
