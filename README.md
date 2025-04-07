# pygcp

#### **Purpose:**
A library containing useful functions for interacting with Google Cloud Platform (GCP) and Google Workspace tools with Python.

#### **Supported platforms:**
- Google BigQuery
- Google Cloud Storage Bucket
- Google Drive

---

## Installation

### Windows WSL

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.1.1 --break-system-packages
```

### Windows WSL (force reinstallation)

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.1.1 --break-system- --force-reinstall
```


### macOS/Linux

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.1.1
```

### macOS/Linux ((force reinstallation))

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.1.1 --force-reinstall
```

---

## ```pygcp.bigquery```

### **bq_to_df**

#### **Usage:**
- Read SQL script and query data from BigQuery
- Store the query results in a pandas dataframe

#### **Syntax:**

```py
def bq_to_df(bq_client, sql_script:str, log=False, ignore_error=False):
```

#### **Parameters**:

- ```bq_client```: client object for BigQuery
- ```sql_script```: the path to the SQL script to be executed
- ```replace_in_query```: a list of tuples, in the form of (look for a, replace with b) to replace certain components in the query
- ```log```:
	- ```True```: enable logging
	- ```False```: disable logging
- ```ignore_error```:
	- ```True```: returns empty list and proceed when error occurs
	- ```False```: stops execution and raises exception

#### **Return value**:
- type: pandas dataframe
- returns an empty dataframe if error occurs and user chooses to ignore error

---

### **bq_to_excel**

#### **Usage**
- Calls ```bq_to_df``` to get query results in the form of pandas dataframe.
- Slices the dataframe by nth rows.
- Generates multiple versions of ```.xlsx``` binary files. Example: query results from ```exampe.sql``` yields 3 million rows, if sliced by every 1 million row, will generate ```example_1.xlsx```,``` example2.xlsx```, ```example_3.xlsx```.

#### **Syntax**:

```py
def bq_to_excel(bq_client, sql_script:str, slice_row:int, outfile_name:str, log=False, ignore_eror=False) -> tuple:
```

#### **Parameters**:
- ```bq_client```: client object for BigQuery
- ```sql_script```: the name of the SQL script to be executed
- ```slice_row```: slice my nth many rows
- ```outfile_name```: naming convention for output file
	- e.g. from ```example.sql```, generate ```example_{version}.xlsx```, input ```example.csv```.
- ```replace_in_query```: a list of tuples, in the form of (look for a, replace with b) to replace certain components in the query
- ```log```:
	- ```True```: enable logging
	- ```False```: disable logging
- ```ignore_error```:
	- ```True```: returns empty list and proceed when error occurs
	- ```False```: stops execution and raises exception

#### **Return value**:
- type: list of tuples
	- e.g. ```[(filename_1.xlsx, buffer_1), (filename_2.xlsx, buffer_2), ...]```
- note: the excel files are stored as binary data in a temporary in RAM and only exists during runtime

---

### **bq_to_csv**

#### **Usage**
- Calls ```bq_to_df``` to get query results in the form of pandas dataframe.
- Slices the dataframe by nth rows.
- Generates multiple versions of ```.csv``` binary files. Example: query results from ```exampe.sql``` yields 3 million rows, if sliced by every 1 million row, will generate ```example_1.csv```,``` example2.csv```, ```example_3.csv```.

#### **Syntax:**

```py
def bq_to_csv(bq_client, sql_script:str, slice_row:int, outfile_name:str, log=False, ignore_eror=False) -> tuple:
```

#### **Parameters**:
- ```bq_client```: client object for BigQuery
- ```sql_script```: the name of the SQL script to be executed
- ```slice_row```: slice my nth many rows
- ```outfile_name```: naming convention for output file
	- e.g. from ```example.sql```, generate ```example_{version}.xlsx```, input ```example.csv```.
- ```replace_in_query```: a list of tuples, in the form of (look for a, replace with b) to replace certain components in the query
- ```log```:
	- ```True```: enable logging
	- ```False```: disable logging
- ```ignore_error```:
	- ```True```: returns empty list and proceed when error occurs
	- ```False```: stops execution and raises exception

#### **Return value**:
- type: list of tuples
	- e.g. ```[(filename_1.csv, buffer_1), (filename_2.csv, buffer_2), ...]```
- note: the excel files are stored as binary data in a temporary in RAM and only exists during runtime

---

### **df_to_bq**

#### **Ussage**:
- Load data from a pandas dataframe to designated tables in BigQuery

#### **Syntax:**

```py
def df_to_bq(bq_client, df, table_path:str, mode:str):
```

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
def drive_autodetect_folders(service, parent_folder_id:str, folder_name:str, create_folder:bool):
```

#### **Parameters**:

- ```service```: Google Drive service object
- ```parent_folder_id```: the folder ID of the folder preceeding the target folder
- ```folder_name```: the name of the target folder
- ```create_folder```: boolean value to determine folder creation

#### **Return value**
- type: dictionary
- the dicationary contains the detected/created target folder ID, folder name and last modified time 
- returns an empty dictionary if folder is not detected and not created

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

### **```drive_search_filename```**

#### **Usage**:

#### **Syntax**:

```py
def drive_search_filename(service, parent_folder_id: str, file_name:str):
```

#### **Parameters**:
- ```service```: Google Drive service object
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

### **```build_drive_service```**

#### **Usage**:

#### **Syntax**:

#### **Parameters**:

#### **Return value**

---

### **```drive_excel_to_df```**

### **```build_drive_service```**

#### **Usage**:

#### **Syntax**:

#### **Parameters**:

#### **Return value**

---

### **```local_excel_to_gdrive```**

### **```build_drive_service```**

#### **Usage**:

#### **Syntax**:

#### **Parameters**:

#### **Return value**

---

### **```local_csv_to_gdrive```**

### **```build_drive_service```**

#### **Usage**:

#### **Syntax**:

#### **Parameters**:

#### **Return value**

---
