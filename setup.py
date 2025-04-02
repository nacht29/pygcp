from setuptools import setup, find_packages

setup(
	name="pygcp",
	version="0.1.0",  # Use semantic versioning (e.g., 0.1.0, 1.0.0)
	author="Chan Yan Zhe",
	author_email="yanzhechan29@gmail.com",
	description="A Python library for Google Cloud Platform (GCP) and Google Workspace related operations",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/yourusername/pygcp",
	packages=find_packages(),
	install_requires=[
    "pandas",
    "google-cloud-bigquery",
    "google-cloud-storage",   
    "google-api-python-client",
    "google-auth",
    "protobuf>=3.20.0,<4.0.0"
],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires=">=3.10",
)