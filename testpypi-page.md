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
