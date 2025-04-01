from google.cloud import storage

def local_excel_to_bucket(bucket_client, bucket_id:str, filepath_in_bucket:str, excel_buffer, log=True):
	try:
		bucket = bucket_client.get_bucket(bucket_id)
	except Exception:
		if log:
			log.error(f'Failed to detect Bucket')
		raise

	try:
		blob = bucket.blob(filepath_in_bucket)
		blob.upload_from_file(
			excel_buffer,
			content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
		)
	except Exception:
		if log:
			log.error('Failed to upload file to bucket')
		raise

def local_excel_to_bucket(bucket_client, bucket_id:str, filepath_in_bucket:str, csv_buffer, log=True):
	try:
		bucket = bucket_client.get_bucket(bucket_id)
	except Exception:
		if log:
			log.error(f'Failed to detect Bucket')
		raise

	try:
		blob = bucket.blob(filepath_in_bucket)
		blob.upload_from_file(
			csv_buffer,
			content_type='text/csv'
		)
	except Exception:
		if log:
			log.error('Failed to upload file to bucket')
		raise