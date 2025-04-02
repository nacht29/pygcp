import pandas as pd
from io import BytesIO
from datetime import datetime
from google.cloud import bigquery as bq
from google.oauth2 import service_account

'''
BigQuery- Extract/Query from BQ
'''

def bq_to_df(bq_client, sql_script:str, log=False, ignore_error=False):
	with open(sql_script, 'r') as cur_script:
		if log:
			print(f'\n\n{datetime.now()} Query: {sql_script}')

		try:
			query = ' '.join([line for line in cur_script])
			results_df = bq_client.query(query).to_dataframe()
		except Exception:
			print(f'{sql_script} query failed.')
			if ignore_error:
				results_df = pd.DataFrame() 
				return results_df
			raise

		if log:
			print(f'Results: {results_df.shape}')

	return (results_df)

# read SQL script and query data from BQ
# write data to excel binary
# returns [(filename1, buffer1), (filename2, buffer2), ...]
def bq_to_excel(bq_client,
				sql_script:str,
				slice_row:int,
				outfile_name:str,
				log=False,
				ignore_eror=False
) -> tuple:

	if not 0 < slice_row <= 1000000:
		raise ValueError('Invalid slice length.')

	results_df = bq_to_df(bq_client, sql_script, log, ignore_eror)
	excel_buffers  = []

	# slice the results of each script
	for cur_row in range(0, len(results_df), slice_row):
		file_ver = cur_row // slice_row + 1
		subset_df = results_df.iloc[cur_row:cur_row + slice_row]
		outfile_name = outfile_name.replace('.xlsx', f'_{file_ver}.xlsx')

		print(f'{datetime.now()} creating xlsx binary for {outfile_name}')

		# init binary buffer for xlsx file
		cur_buffer = BytesIO()

		with pd.ExcelWriter(cur_buffer, engine='xlsxwriter') as writer:
			subset_df.to_excel(writer, index=False, header=True)
		cur_buffer.seek(0)

		# add the buffer data and file name to the main list
		excel_buffers.append((outfile_name, cur_buffer))

		print(f'{datetime.now()} {outfile_name} binary created')

	return excel_buffers

def bq_to_csv(bq_client,
			  sql_script:str,
			  slice_row:int,
			  outfile_name:str,
			  log=False,
			  ignore_error=False
) -> tuple:

	if not 0 < slice_row <= 1000000:
		raise ValueError('Invalid slice length.')

	results_df = bq_to_df(bq_client, sql_script, log, ignore_error)
	csv_buffers = []

	for cur_row in range(0, len(results_df), slice_row):
		file_ver = cur_row // slice_row + 1
		subset_df = results_df.iloc[cur_row:cur_row + slice_row]
		cur_outfile_name = outfile_name.replace('.csv', f'_{file_ver}.csv')

		print(f'{datetime.now()} creating CSV binary for {cur_outfile_name}')

		cur_buffer = BytesIO()
		subset_df.to_csv(cur_buffer, index=False)
		cur_buffer.seek(0)

		csv_buffers.append((cur_outfile_name, cur_buffer))

		print(f'{datetime.now()} {cur_outfile_name} CSV binary created')

	return csv_buffers

'''
BigQuery - Load to BQ
'''

def df_to_bq(bq_client, df, table_path:str, mode:str):
	if mode == 'a':
		write_disposition = 'WRITE_APPEND'
	elif mode == 't':
		write_disposition ="WRITE_TRUNCATE"
	else:
		raise ValueError(f"{mode} is not recognised. Use 'a' for append or 't' for truncate")

	try:
		job_config = bq.LoadJobConfig(write_disposition='WRITE_TRUNCATE', autodetect=True)
		bq_client.load_table_from_dataframe(df, table_path, job_config=job_config)
	except Exception:
		raise
