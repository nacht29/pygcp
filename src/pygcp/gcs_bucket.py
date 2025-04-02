from google.cloud import storage
from google.oauth2 import service_account

'''
Build Bucket Client
'''

def build_bucket_client(service_account:str):
	credentials = service_account.Credentials.from_service_account_file(service_account)
	bucket_client = storage.Client(credentials=credentials, project=credentials.project_id)
	return bucket_client

'''
Load to Bucket
'''
# bucket path: gch_extract_drive_01/supply_chain/possales_rl
# bucket_id: gch_extract_drive_01
# bucket_base_filepath: supply_chain/possales_rl 
def local_excel_to_bucket(
	bucket_client,
	bucket_id:str,
	bucket_base_filepath:str,
	excel_files:tuple,
	content_type:str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
	log=True
):
	try:
		bucket = bucket_client.get_bucket(bucket_id)
	except Exception:
		if log:
			print(f'Failed to access bucket {bucket_id}')
		raise

	for filename, buffer in excel_files:
		try:
			# full_path = f"{bucket_base_filepath}/{filename}" if bucket_base_filepath else filename
			if bucket_base_filepath:
				full_path = f"{bucket_base_filepath}/{filename}"
			else:
				full_path = filename

			blob = bucket.blob(full_path)
			blob.upload_from_file(
				buffer,
				content_type=content_type
			)

			if log:
				print(f"Uploaded {filename} to gs://{bucket_id}/{full_path}")

		except Exception:
			if log:
				print(f'Failed to upload {filename}')
			raise

def local_csv_to_bucket(
	bucket_client,
	bucket_id:str,
	bucket_base_filepath:str,
	csv_files:tuple,
	content_type:str = 'text/csv',
	log=True
):
	try:
		bucket = bucket_client.get_bucket(bucket_id)
	except Exception as e:
		if log:
			print(f'Failed to access bucket {bucket_id}: {str(e)}')
		raise

	for filename, buffer in csv_files:
		try:
			# full_path = f"{bucket_base_filepath}/{filename}" if bucket_base_filepath else filename
			if bucket_base_filepath:
				full_path = f"{bucket_base_filepath}/{filename}"
			else:
				full_path = filename

			blob = bucket.blob(full_path)
			blob.upload_from_file(
				buffer,
				content_type=content_type
			)

			if log:
				print(f"Uploaded {filename} to gs://{bucket_id}/{full_path}")

		except Exception:
			if log:
				print(f'Failed to upload {filename}')
			raise

'''
Bucket to BQ
'''

def bucket_csv_to_bq(bq_client, bucket_csv_path:str, project_id:str, dataset:str, table:str, mode:str):
	if mode == 'a':
		write_disposition = 'WRITE_APPEND'
	elif mode == 't':
		write_disposition ="WRITE_TRUNCATE"
	else:
		raise ValueError(f"{mode} is not recognised. Use 'a' for append or 't' for truncate")
	
	job_config = bq.LoadJobConfig(
		source_format=bq.SourceFormat.CSV,
		skip_leading_rows=1,
		autodetect=True,
		write_disposition=write_disposition
	)

	uri = f'gs://{bucket_csv_path}'
	try:
		bq_client.load_table_from_uri(uri, f"{project_id}.{dataset}.{table}", job_config=job_config)
	except Exception:
		print('Failed to load CSV to bucket')
		raise

def bucket_excel_to_bq(bq_client, bucket_excel_path:str, project_id:str, dataset:str, table:str, mode:str):

	if mode == 'a':
		write_disposition = 'WRITE_APPEND'
	elif mode == 't':
		write_disposition ="WRITE_TRUNCATE"
	else:
		raise ValueError(f"{mode} is not recognised. Use 'a' for append or 't' for truncate")
	
	job_config = bq.LoadJobConfig(
		source_format=bq.SourceFormat.XLSX,
		skip_leading_rows=1,
		autodetect=True,
		write_disposition=write_disposition
	)

	uri = f'gs://{bucket_excel_path}'
	try:
		bq_client.load_table_from_uri(uri, f"{project_id}.{dataset}.{table}", job_config=job_config)
	except Exception:
		print('Failed to load Excel to bucket')
		raise