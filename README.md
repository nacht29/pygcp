# pygcp

**[TestPyPI Page](https://test.pypi.org/project/pygcp/)**

#### **Purpose:**
A library containing useful functions for interacting with Google Cloud Platform (GCP) and Google Workspace tools with Python.

#### **Supported platforms:**
- Google BigQuery
- Google Cloud Storage Bucket
- Google Drive

**[View the project on TestPyPI](https://test.pypi.org/project/pygcp/)**

---

## Installation

### Windows WSL

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.2.4 --break-system-packages
```

### Windows WSL (force reinstallation)

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.2.4 --break-system- --force-reinstall
```


### macOS/Linux

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.2.4
```

### macOS/Linux (force reinstallation)

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.2.4 --force-reinstall
```

---

## ```pygcp.bigquery```

### **bq_to_df**

#### **Usage:**
- Read SQL script and query data from BigQuery
- Store the query results in a pandas dataframe

#### **Syntax:**

```py
def bq_to_df(bq_client, sql_script:str, replace_in_query:list=[], log=False, ignore_error=False):
```

#### **Parameters**:

- ```bq_client```: client object for BigQuery
- ```sql_script```: the path to the SQL script to be executed
- ```replace_in_query```: a list of tuples, in the form of (look for a, replace with b) to replace certain components in the query
- ```log```: boolean value to enable or disable logging
- ```ignore_error```:
	- ```True```: returns empty list and proceed when error occurs
	- ```False```: stops execution and raises exception

#### **Return value**:
- type: pandas dataframe
- returns an empty dataframe if error occurs and user chooses to ignore error

---

### **bq_to_excel**

```py
def bq_to_excel(bq_client, sql_script:str, slice_row:int, outfile_name:str, replace_in_query:list=[], sep=',', log=False, ignore_eror=False): -> tuple:
```

#### **Usage**
- Calls ```bq_to_df``` to get query results in the form of pandas dataframe.
- Slices the dataframe by nth rows.
- Generates multiple versions of ```.xlsx``` binary files. Example: query results from ```exampe.sql``` yields 3 million rows, if sliced by every 1 million row, will generate ```example_1.xlsx```,``` example2.xlsx```, ```example_3.xlsx```.

#### **Parameters**:
- ```bq_client```: client object for BigQuery
- ```sql_script```: the name of the SQL script to be executed
- ```slice_row```: slice my nth many rows
- ```outfile_name```: naming convention for output file
	- e.g. from ```example.sql```, generate ```example_{version}.xlsx```, input ```example.csv```.
- ```replace_in_query```: a list of tuples, in the form of (look for a, replace with b) to replace certain components in the query
- ```log```: boolean value to enable or disable logging
- ```ignore_error```:
	- ```True```: returns empty list and proceed when error occurs
	- ```False```: stops execution and raises exception

#### **Return value**:
- type: list of tuples
	- e.g. ```[(filename_1.xlsx, buffer_1), (filename_2.xlsx, buffer_2), ...]```
- note: the excel files are stored as binary data in a temporary in RAM and only exists during runtime

---

### **bq_to_csv**

```py
def bq_to_csv(bq_client, sql_script:str, slice_row:int, outfile_name:str, replace_in_query:list=[], sep:str=',', log:str=False, ignore_eror:str=False): -> tuple:
```

#### **Usage**
- Calls ```bq_to_df``` to get query results in the form of pandas dataframe.
- Slices the dataframe by nth rows.
- Generates multiple versions of ```.csv``` binary files. Example: query results from ```exampe.sql``` yields 3 million rows, if sliced by every 1 million row, will generate ```example_1.csv```,``` example2.csv```, ```example_3.csv```.

#### **Parameters**:
- ```bq_client```: client object for BigQuery
- ```sql_script```: the name of the SQL script to be executed
- ```slice_row```: slice my nth many rows
- ```outfile_name```: naming convention for output file
	- e.g. from ```example.sql```, generate ```example_{version}.xlsx```, input ```example.csv```.
- ```replace_in_query```: a list of tuples, in the form of (look for a, replace with b) to replace certain components in the query
- ```sep```: delimiter for the CSV file
- ```encoding```: encoding type for CSV file, UTF8 by default
- ```log```: boolean value to enable or disable logging
- ```ignore_error```:
	- ```True```: returns empty list and proceed when error occurs
	- ```False```: stops execution and raises exception

#### **Return value**:
- type: list of tuples
	- e.g. ```[(filename_1.csv, buffer_1), (filename_2.csv, buffer_2), ...]```
- note: the excel files are stored as binary data in a temporary in RAM and only exists during runtime

---

### **df_to_bq**

```py
def df_to_bq(bq_client, df, table_path:str, mode:str):
```

#### **Ussage**:
- Load data from a pandas dataframe to designated tables in BigQuery

#### **Parameters**:
- ```bq_client```: BigQuery client object
- ```tabl_path```: the exact path to the destination table, in the format of ```project_id.dataset.table_name```.
- ```mode```: 't' for truncate and 'a' for append

#### **Return value**:
- No return values

---

## ```pygcp.google-drive```

### **```build_drive_service```**

#### **Usage**:
- Creates an authenticated service object to make authorized API calls to Google Drive
- Needed by most functions that read and write files in Google Drive

#### **Syntax**:

```py
def build_drive_service(service_account_key):
```

#### **Parameters**:
- ```service_account_key````: Path to the JSON key of the authenticated Service Account

#### **Return value**
- Google Drive service object

---

### **```drive_autodetect_folders```**

#### **Usage**:
- Searches for a target folder by name in Google Drive
- User can choose to create the folder if target folder does not exist

#### **Syntax**:

```py
def drive_autodetect_folders(service, is_shared_drive:bool, parent_folder_id:str, folder_name:str, create_folder:bool):
```

#### **Parameters**:

- ```service```: Google Drive service object
- ```is_shared_drive```: ```True``` if the Drive is a Shared Drive else ```False```
- ```parent_folder_id```: the folder ID of the folder preceeding the target folder
- ```folder_name```: the name of the target folder
- ```create_folder```: boolean value to determine folder creation

#### **Return value**
- type: dictionary
- the dicationary contains the detected/created target folder ID, folder name and last modified time 
- returns an empty dictionary if folder is not detected and not created
- note that both folders and files are identified by a file Id, accessed by ```files['id']```
- Drive considers folders as a file as well, with ```'mimeType': 'application/vnd.google-apps.folder'```

	```py
	{
		"files": [
			{
				"id": "your-folder-fileId",
				"name": "your-folder-name",
				"modifiedTime": "ISO-8601-timestamp"
			}
		]
	}
	```

---

### **```drive_search_filename```**

#### **Usage**:

#### **Syntax**:

```py
def drive_search_filename(service, is_shared_drive:bool, parent_folder_id: str, file_name:str):
```

#### **Parameters**:
- ```service```: Google Drive service object
- ```is_shared_drive```: ```True``` if the Drive is a Shared Drive else ```False```
- ```parent_folder_id```: the folder ID of the folder preceeding the target folder
- ```file_name```: name of the target file 

#### **Return value**
- type: dictionary
- the dicationary contains the detected target file ID, file name and last modified time 
- returns an empty dictionary if file is not detected

	```py
	{
		"files": [
			{
				"id": "your-file-id",
				"name": "your-file-name",
				"modifiedTime": "ISO-8601-timestamp"
			}
		]
	}
	```

---

### **```drive_csv_to_df```**

```py
def drive_csv_to_df(service, file_metadata:dict, raise_error:bool=True, log:bool=True):
```

#### **Usage**:
Read CSV file data from Google Drive and write the data to a pandas dataframe.


#### **Parameters**:

- ```service```: Google Drive service object
- ```is_shared_drive```: ```True``` if the Drive is a Shared Drive else ```False```is_shared_drive:bool, 
- ```file_metadata```: properties of the CSV file to be read, obtained from functions such as ```drive_search_filename```.
- ```raise_error```: raise or ignore errors

#### **Return value**
- type: pandas dataframe
- returns a dataframe with data
- returns an empty dataframe if error occurs and user chooses to ignore the error

---

### **```drive_excel_to_df```**

```py
def drive_excel_to_df(service, is_shared_drive:bool, file_metadata:dict, raise_error:bool=True, log:bool=True):
```

#### **Usage**:
Read Excel file data from Google Drive and write the data to a pandas dataframe.

#### **Parameters**:

- ```service```: Google Drive service object
- ```is_shared_drive```: ```True``` if the Drive is a Shared Drive else ```False```
- file_metadata: properties of the Excel file to be read, obtained from functions such as ```drive_search_filename```.
- ```raise_error```: raise or ignore errors
- ```log```: boolean value to enable or disable logging

#### **Return value**
- type: pandas dataframe
- returns a dataframe with data
- returns an empty dataframe if error occurs and user chooses to ignore the error

---

### **```local_excel_to_gdrive```**

```py
def local_excel_to_gdrive(service, main_drive_id:str, is_shared_drive:bool, dst_folder_id:str, excel_files:list, update_dup:bool=True, log:bool=False):
```

#### **Usage**:

Load binary Excel files stored in local DRAM to Google Drive.

#### **Parameters**:

- ```service```: Google Drive service object
- ```main_drive_id```: ID of the Drive containing the target folder, only needed for shared Drives
- ```is_shared_drive```: ```True``` if the Drive is a Shared Drive else ```False```
- ```dst_folder_id```: folder ID of the folder to upload the file to
- ```excel_files```: List of Excel file name and buffers, typically gotten from ```pygcp.bigquery.bq_to_excel``` function
- ```update_dup```: ```True``` to update data into existing files, ```False``` to create a new file despite duplicates 
- ```log```: ```True``` to enable and ```False``` to disable logging

#### **Return value**

- no return values

---

### **```local_csv_to_gdrive```**

```py
def local_csv_to_gdrive(service, main_drive_id:str, is_shared_drive:bool, dst_folder_id:str, csv_files:list, update_dup=True, log=False):
```

#### **Usage**:

Load binary CSV files stored in local DRAM to Google Drive.

#### **Parameters**:

- ```service```: Google Drive service object
- ```main_drive_id```: ID of the Drive containing the target folder, only needed for shared Drives
- ```is_shared_drive```: ```True``` if the Drive is a Shared Drive else ```False```
- ```dst_folder_id```: folder ID of the folder to upload the file to
- ```csv_files```: List of CSV file name and buffers, typically gotten from ```pygcp.bigquery.bq_to_csv``` function
- ```update_dup```: ```True``` to update data into existing files, ```False``` to create a new file despite duplicates 
- ```log```: ```True``` to enable and ```False``` to disable logging

#### **Return value**

- no return values

---

## ```pygcp.google-drive```

### ```local_excel_to_bucket```

#### **Usage**:
- Load binary Excel files stored in local DRAM to Google Cloud Storage Bucket

#### **Syntax**:

```py
def local_excel_to_bucket(bucket_client, bucket_id:str, bucket_base_filepath:str, excel_files:tuple, content_type:str="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", log=True):
```

#### **Parameters**:
- ```bucket_client```: client object for GCS Bucket
- ```bucket_id```: GCS Bucket bucket id
- ```bucket_base_filepath```: full path to the directory in GCS Bucket to which the Excel file will be uploaded
- ```excel_files```: List of Excel file name and buffers, typically gotten from ```pygcp.bigquery.bq_to_excel``` function
- ```log```: boolean value to enable or disable logging

#### **Return value**
- No return value

---

### ```local_csv_to_bucket```

#### **Usage**:
- Load binary CSV files stored in local DRAM to Google Cloud Storage Bucket

#### **Syntax**:

```py
def local_csv_to_bucket(bucket_client, bucket_id:str, bucket_base_filepath:str, csv_files:tuple, content_type:str="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", log=True):
```

#### **Parameters**:
- ```bucket_client```: client object for GCS Bucket
- ```bucket_id```: GCS Bucket bucket id
- ```bucket_base_filepath```: full path to the directory in GCS Bucket to which the CSV file will be uploaded
- ```excel_files```: List of Excel file name and buffers, typically gotten from ```pygcp.bigquery.bq_to_excel``` function
- ```log```: boolean value to enable or disable logging

#### **Return value**
- No return value
