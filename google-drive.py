import pandas as pd
import logging as log
from io import BytesIO
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

'''
Creds and utils
'''

def build_drive_service(service_account:str, scope:str):
	creds = service_account.Credentials.from_service_account_file(service_account, scopes=scope)
	service = build('drive', 'v3', credentials=creds)
v
def drive_get_dup_files(service, dst_folder_id:str, out_filename:str):
	query = f"""
	'{dst_folder_id}' in parents
	and name='{out_filename}'
	and trashed=false
	"""

	results = service.files().list(
			q=query,
			fields='files(id, name)',
			supportsAllDrives=True
	).execute()

	# get dup file id
	dup_files = results.get('files')

	return dup_files

def drive_create_file(service, file_metadata:dict, media, log=False):
	if log:
		log.info(f"{datetime.now()} Creating {file_metadata['name']}")

	service.files().create(
		body=file_metadata,
		media_body=media,
		fields='id',
		supportsAllDrives=True
	).execute()

def drive_update_file(service, media, dup_files:list, log:bool):
	if log:
		log.info(f"{datetime.now()} Updating {dup_files[0]['name']}")

	dup_file_id = dup_files[0]['id']
	service.files().update(
		fileId=dup_file_id,
		media_body=media,
		supportsAllDrives=True
	).execute()

'''
Search/Autodetect
'''

# detect existing folder or create new folder
# return latest occurence of existing folder metadata in dst
# parent_folder_id = folder id before the target folder
def drive_autodetect_folders(service, parent_folder_id:str, folder_name:str, create_folder:bool):
	query = f"""
	'{parent_folder_id}' in parents 
	and name='{folder_name}'
	and mimeType='application/vnd.google-apps.folder' 
	and trashed=false
	"""

	# execute the query
	results = service.files().list(
		q=query,
		fields='files(id, name, modifiedTime)',
		orderBy='modifiedTime desc',
		pageSize=1,
		supportsAllDrives=True,
		includeItemsFromAllDrives=True
	).execute()

	folders_in_drive = results.get('files', []) # files_in_drive = results.get('files', [])

	if folders_in_drive:
		return folders_in_drive[0]
	elif not folders_in_drive and create_folder:
		folder_metadata = {
			'name': folder_name,
			'mimeType': 'application/vnd.google-apps.folder',
			'parents': [parent_folder_id]
		}

		folder = service.files().create(
			body=folder_metadata,
			fields='id, name',
			supportsAllDrives=True
			# note that for .create, there is no need to includeItemsFromAllDrives=True
		).execute()

		return folder

	return []

# return latest occurence of file metadata
def drive_search_filename(service, parent_folder_id: str, file_name:str):
	query = f"""
	'{parent_folder_id}' in parents
	and name = '{file_name}'
	and trashed=false
	"""
	
	try:
		response = service.files().list(
			q=query,
			fields='files(id, name, modifiedTime)',
			orderBy='modifiedTime desc',
			pageSize=1,
			supportsAllDrives=True,
			includeItemsFromAllDrives=True,
		).execute()
		
		files = response.get('files', [])
		if files:
			return files[0]
		else:
			return []
			
	except Exception:
		return []

'''
Extract to df
'''

# extract to df - can be used to push to bq/bucket
def drive_csv_to_df(service, file_metadata, raise_error=True, log=True):
	try:
		request = service.files().get_media(fileId=file_metadata['id'])
		csv_buffer = BytesIO()
		downloader = MediaIoBaseDownload(csv_buffer, request)

		while True:
			status, done = downloader.next_chunk()
			log.info(f"{file_metadata['name']} {int(status.progress() * 100)}%")
			if done:
				break

		csv_buffer.seek(0)
		results_df = pd.read_csv(csv_buffer)

		return results_df

	except Exception as error:
		if log:
			log.info(f"Error processing {file_metadata['name']}: {error}")
		if raise_error:
			raise
		return pd.DataFrame()

# extract to df - can be used to push to bq/bucket
def drive_excel_to_df(service, file_metadata:dict, raise_error=True, log=True):
	try:
		request = service.files().get_media(fileId=file_metadata['id'])
		excel_buffer = BytesIO()
		downloader = MediaIoBaseDownload(excel_buffer, request)

		while True:
			status, done = downloader.next_chunk()
			log.info(f"{file_metadata['name']} {int(status.progress() * 100)}%")
			if done:
				break

		excel_buffer.seek(0)
		results_df = pd.read_excel(excel_buffer)

		return results_df

	except Exception as error:
		if log:
			log.info(f"Error processing {file_metadata['name']}: {error}")
		if raise_error:
			raise
		return pd.DataFrame()

'''
Load local
'''

# used in conjunction wtih functions bq_to_excel()
# bq_to_excel() returns a list of excel_buffers()
def local_excel_to_gdrive(
		service,
		main_drive_id:str,
		dst_folder_id:str,
		excel_buffers:list,
		out_filename:str,
		update_dup=True,
		log=False
):
	for excel_buffer in excel_buffers:
		# define file metadata and media type
		file_metadata = {
			'name': out_filename,
			'parents': [dst_folder_id],
			'driveId': main_drive_id
		}

		media = MediaIoBaseUpload(
			excel_buffer,
			mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
			resumable=True
		)

		if update_dup:
			dup_files = drive_get_dup_files(service, dst_folder_id, out_filename)

			# update existing files or create new ones
			if dup_files:
				drive_update_file(service, media, dup_files, log)
			else:
				drive_create_file(service, file_metadata, media)

		else:
			drive_create_file(service, file_metadata, media)

# used in conjunction wtih functions bq_to_csv
def local_csv_to_gdrive(
		service,
		main_drive_id:str,
		dst_folder_id:str,
		csv_buffers:list,
		out_filename:str,
		update_dup=True,
		log=False
):
	for csv_buffer in csv_buffers:
		# define file metadata and media type
		file_metadata = {
			'name': out_filename,
			'parents': [dst_folder_id],
			'driveId': main_drive_id
		}

		media = MediaIoBaseUpload(
			csv_buffer,
			mimetype='text/csv',
			resumable=True
		)

		if update_dup:
			dup_files = drive_get_dup_files(service, dst_folder_id, out_filename)

			# update existing files or create new ones
			if dup_files:
				drive_update_file(service, media, dup_files, log)
			else:
				drive_create_file(service, file_metadata, media)

		else:
			drive_create_file(service, file_metadata, media)
