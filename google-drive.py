import logging as log
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

def build_drive_service(service_account:str, scope:str):
	creds = service_account.Credentials.from_service_account_file(service_account, scopes=scope)
	service = build('drive', 'v3', credentials=creds)

# parent_folder_id = folder id of the folder preceding the folder you are trying to find
# say you want to detect folder1/dst_folder:
# drive_autodetect_folders(service, folder1 folder id, dst_folder)
def drive_autodetect_folders(service, parent_folder_id:str, folder_name:str):
	'''
	# searches if folder exists in drive
	# returns a list of dict
	# id = file/folder id
	# name = file/folder name
	files = [
		{'id':0, 'name':'A'},
		{'id':1, 'name':'B'}
	]
	'''

	# get all folder names in dest
	# parent_folder_id: folder id folder right before the dest folder
	query = f"""
	'{parent_folder_id}' in parents 
	and name='{folder_name}'
	and mimeType='application/vnd.google-apps.folder' 
	and trashed=false
	"""

	# execute the query
	results = service.files().list(
		q=query,
		fields='files(id,name)',
		supportsAllDrives=True, # required when accessing shared drives
		includeItemsFromAllDrives=True # ONLY NEEDED FOR '''.list()''' method!!!
	).execute()
	files_in_drive = results.get('files') # files_in_drive = results.get('files', [])

	# return dest folder id if detected
	# create dest folder if not yet created
	# this is the dynamic folder creation
	if files_in_drive:
		return files_in_drive[0]['id']
	else:
		file_metadata = {
			'name': folder_name,
			'mimeType': 'application/vnd.google-apps.folder',
			'parents': [parent_folder_id]
		}

		folder = service.files().create(
			body=file_metadata,
			fields='id',
			supportsAllDrives=True # required when accessing shared drives
			# note that for .create, there is no need to includeItemsFromAllDrives=True
		).execute()

		return folder['id']

def local_excel_gdrive(service, main_drive_id: str, dst_folder_id:str, excel_buffer, out_filename:str):
	
	query = f"""
	'{dst_folder_id}' in parents
	and name = '{out_filename}'
	and trashed=false
	"""


	results = service.files().list(
			q=query,
			fields='files(id, name)',
			supportsAllDrives=True
	).execute()

	# get dup file id
	dup_files = results.get('files')

	# xlsx file metadata
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

	# update or create files
	if dup_files:
		log.info(f"{datetime.now()} Updating {dup_files[0]['name']}")
		dup_file_id = dup_files[0]['id']
		file = service.files().update(
			fileId=dup_file_id,
			media_body=media,
			supportsAllDrives=True
		).execute()

	else:
		service.files().create(
			body=file_metadata,
			media_body=media,
			fields='id',
			supportsAllDrives=True
		).execute()

def local_csv_gdrive(service, main_drive_id: str, dst_folder_id:str, csv_buffer, out_filename:str):
	pass
