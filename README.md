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
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp --break-system-packages
```

### Windows WSL (force reinstallation)

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp --break-system- --force-reinstall
```


### macOS/Linux

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp
```

### macOS/Linux ((force reinstallation))

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp --force-reinstall
```

---

## ```pygcp.bigquery```

### **bq_to_df**

#### **Usage:**
Read SQL script and query data from BigQuery then stores the query results in a pandas dataframe.

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

### **bq_to_excel**

---

## ```pygcp.google-drive```

**Functions for interacting with Google Drive**

---
