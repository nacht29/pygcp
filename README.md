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
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.1.0 --break-system-packages
```

### Windows WSL (force reinstallation)

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.1.0 --break-system- --force-reinstall
```


### macOS/Linux

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.1.0
```

### macOS/Linux ((force reinstallation))

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.1.0 --force-reinstall
```

---

## Setup ENV

1. **In the terminal, type:**

	```bash
	pip show pygcp
	```

	This returns the path where the pygcp package is installed, such as on Linux/WSL: ```/home/username/.local/lib/python3.12/site-packages```

2. Open command palette (```Ctrl + Shift + P``` on Windows/Linux and ```Cmd + Shift + P``` on macOS). Then, type:

	```
	Preferences: Open Workspace Settings (JSON)
	```

	Add the following to your workspace settings:

	```json
	"settings": {
			"python.analysis.extraPaths": [
				"/home/nacht29/.local/lib/python3.12/site-packages"
			],
			"python.defaultInterpreterPath": "/usr/bin/python3",
			"python.analysis.diagnosticSeverityOverrides": {
				"reportMissingImports": "none"
			}
		}
	```

3. Open command palette and type: 
	
	```
	Python: Select Interpreter
	``` 
	
	then select
	
	```
	Use Python from 'pyton.defaultInterpreterPath' setting
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
- ```sql_script```: the name of the SQL script to be executed
- ```log```:
	- ```True```: enable
	- ```False```: disable logging
- ```ignore_error```:
	- ```True```: returns empty list and proceed when error occurs
	- ```False```: stops execution and raises exception

#### **Return value**:
- type: pandas dataframe

---

### **bq_to_excel**

#### **Usage**
- Calls ```bq_to_df``` to get query results in the form of pandas dataframe.
- Slices the dataframe by nth rows.
- Generates multiple versions of ```.xlsx``` binary files. Example: query results from ```exampe.sql``` yields 3 million rows, if sliced by every 1 million row, will generate ```example_1.xlsx```,``` example2.xlsx```, ```example_3.xlsx```.

#### **Syntax:**

```py
def bq_to_excel(bq_client, sql_script:str, slice_row:int, outfile_name:str, log=False, ignore_eror=False) -> tuple:
```

#### **Parameters**:
- ```bq_client```: client object for BigQuery
- ```sql_script```: the name of the SQL script to be executed
- ```slice_row```: slice my nth many rows
- ```outfile_name```: naming convention for output file
	- e.g. from ```example.sql```, generate ```example_{version}.xlsx```, input ```example.csv```.
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
	- e.g. from ```example.sql```, generate ```example_{version}.csv```, input ```example.csv```.
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

---

