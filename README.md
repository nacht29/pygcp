# pygcp

#### **Purpose:**
A library containing useful functions for interacting with Google Cloud Platform (GCP) and Google Workspace tools with Python.

#### **Supported platforms:**
- Google BigQuery
- Google Cloud Storage Bucket
- Google Drive

---

## ```pygcp.bigquery```

**Functions for interacting with Google BigQuery**

### bq_to_xlsx

#### **Usage:**

Reads data from BigQuery using a given SQL script and slices the resulting data into multiple Excel (xlsx) binary files of a specified row length.

#### **Syntax:**

```py
def bq_to_xlsx(bq_client, sql_script: str, slice_row: int, outfile_name:str)
```

#### **Parameters**:
- ```bq_client```: The BigQuery client object used for querying data.
- ```sql_script``` (str): The path to your SQL script.
- ```slice_row``` (int): The maximum number of rows each Excel file should contain. Range: ```0 < row <= 1,000,000```
- ```outfile_name``` (str): The base name of the output Excel file. The function appends a version number (_1, _2, etc.) to this base name.

#### **Extra notes: BigQuery client object**

```py
JSON_KEYS_PATH = '/path/to/your/service_account/json-key-file'
credentials = service_account.Credentials.from_service_account_file(JSON_KEYS_PATH)
bq_client = bq.Client(credentials=credentials, project=credentials.project_id)
```

---

## ```pygcp.google-drive```

**Functions for interacting with Google Drive**

---
