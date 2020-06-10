# MID PROJECT PR 
## Overall structure:
Step by step details are provided below, but at a high level there are two main locations to edit if you want to change setup for the data acquisition and database creation steps:
* Configuration (S3 Bucket location and S3 key name, local vs. RDS database creation, etc.) for the data acquisition and database creation is stored in /src/config.py.
* For Docker, environment variables (RDS/MYSQL and S3 credentials) should be created in a .env file in the /src directory. This file will be ignored by Git.

## Running data acquisition and database creation locally

Note (added 5/15 after PR originally submitted): To run the code locally, you need to install the packages listed in requirements.txt (in the root directory) or create a virtual environment with those packages installed and run the code in that virtual environment.

### 1. Acquire the data

### Set your S3 credentials

Set environment variables:
* AWS_ACCESS_KEY_ID = < your AWS access key - for instructions on how to find this, see [here](https://aws.amazon.com/blogs/security/how-to-find-update-access-keys-password-mfa-aws-management-console/) >
* AWS_SECRET_ACCESS_KEY = < your AWS secret access key - for instructions on how to find this, see [here](https://aws.amazon.com/blogs/security/how-to-find-update-access-keys-password-mfa-aws-management-console/) >

Or, when running locally, having a ~./aws/credentials file with the above information will also work.

To acquire the data and upload it in S3, configure the desired data URL, S3 bucket name, and S3 key (the way the data will be labeled in the S3 bucket) in config.py. The default values will download the [COPA data](https://data.cityofchicago.org/Public-Safety/COPA-Cases-Summary/mft5-nfa8) and place it in Laurie's "merrell-copa-cases" bucket with the key "copa_raw_data".

To run the acquisition/S3 upload code with the configured values, navigate into the /src directory and run:

`python acquire_copa_data.py`

**NOTE: This script (when using the default URL) downloads a full file from the Chicago Data Portal. It does not do an API call, it downloads a full CSV of 80k+ rows. PLEASE DO NOT RUN THIS COMMAND REPEATEDLY WITH THE DEFAULT URL, TO AVOID OVERTAXING THE DATA PORTAL SITE. If you want to test the call, please change the RAW_DATA_LOCATION URL in /src/config.py to "https://raw.githubusercontent.com/lauriemerrell/dummy_data/master/dummy_data.txt" - this contains a dummy text file which you can download as much as you want.**

### 2. Create an empty copa_case_attributes table in a database

### Configuration: Local SQLite

When creating the table in a local SQLite database, no credentials are needed. Edit src/config.py with the desired path and database name (DATABASE_PATH - the final portion is the database name.) You do not need to manually construct the engine string. Then, in src/config.py, set the SQLALCHEMY_DATABASE_URI equal to LOCAL_URI.

### Configuration: RDS Instance
To connect to an RDS Instance (for which you have write access), set the local variables MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, and DATABASE_NAME to correspond with valid values for an existing RDS database. To connect to Laurie's default database (specified by default in config.py), you need to be on the Northwestern GlobalProtect VPN. 


## Running data acquisition in Docker
Note that this does not include the database creation code.
### 1. Acquire the data

#### 1. Create environment configuration file

In the /src directory, build a config.env file which will contain your AWS credentials. Specify them like: 

AWS_ACCESS_KEY_ID=< your AWS access key - for instructions on how to find this, see [here](https://aws.amazon.com/blogs/security/how-to-find-update-access-keys-password-mfa-aws-management-console/) >

AWS_SECRET_ACCESS_KEY=< your AWS secret access key - for instructions on how to find this, see [here](https://aws.amazon.com/blogs/security/how-to-find-update-access-keys-password-mfa-aws-management-console/) >

#### 2. Set your configuration

In /src/config.py, configure the S3 bucket to which you would like to upload the data. It must be a bucket to which the user specified above has write access. Set the S3 key you'd like to use to label the data you upload. You can also change the location from which the data is being downloaded if you want. Save your changes.

#### 3. Build the image 

The Dockerfile for running the data acquisition is in the root folder. To build the image, run from root: 

```bash
 docker build -t copa .
```

This command builds the Docker image, with the tag `copa`, based on the instructions in `Dockerfile` and the files existing in this directory.
 
#### 2. Run the container 

To run the data acquisition code, run from root: 

```bash
docker run --env-file ./src/config.env copa
```
**NOTE: This script (when using the default URL) downloads a full file from the Chicago Data Portal. It does not do an API call, it downloads a full CSV of 80k+ rows. PLEASE DO NOT RUN THIS COMMAND REPEATEDLY WITH THE DEFAULT URL, TO AVOID OVERTAXING THE DATA PORTAL SITE. If you want to test the call, please change the RAW_DATA_LOCATION URL in /src/config.py to "https://raw.githubusercontent.com/lauriemerrell/dummy_data/master/dummy_data.txt" and rebuild your Docker image - the new URL contains a dummy text file which you can download as much as you want.**

### 3. Kill the container 

Once finished, you will need to kill the container. To do so: 

```bash
docker kill copa 
```