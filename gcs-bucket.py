from google.cloud import storage

def local_excel_bucket(bucket_client, bucket_id:str, filepath_in_bucket:str, excel_buffer):
	bucket = bucket_client.get_bucket(bucket_id)
	blob = bucket.blob(filepath_in_bucket)
	blob.upload_from_file(
		excel_buffer,
		content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
	)
