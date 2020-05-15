# MSiA423 Template Repository

<!-- toc -->

- [Project charter](#project-charter)
    * [Vision](#vision)
    * [Mission](#mission)
    * [Success criteria](#success-criteria)
- [Directory structure](#directory-structure)
- [Mid-Project PR Instructions](#mid-project-pr)
  * [Data acquisition and database creation - overall structure](#overall-structure)
  * [Running data acquisition and database creation locally](#running-data-acquisition-and-database-creation-locally)
  * [Running data acquisition and database creation in Docker](#running-data-acquisition-and-database-creation-in-docker)

<!-- tocstop -->

# Chicago Civilian Office of Police Accountability Case Outcome Prediction Project


**Developer**: Laurie Merrell

**QA**: Joe Baka

## Project charter

### Vision

Accountability is an important component of the relationship between police departments and the communities in which they operate. One important aspect of this accountability is provided by oversight boards which hear complaints of alleged misconduct by police officers and provide rulings on the merits of these complaints (whether or not they are justified). In Chicago, the Civilian Office of Police Accountability ([COPA](https://www.chicagocopa.org/)) serves this function by hearing cases and deciding whether misconduct occurred (for more information, see COPA's [reference page on the investigative process](https://www.chicagocopa.org/investigations/investigative-process/)). For the public in Chicago to have additional oversight of this process, particularly in the current climate of fraught relationships between police departments and many communities (especially Black communities), it would be useful to have insight on whether complainants of certain races or certain ages are more or less likely to receive favorable outcomes in their complaints than others. This information could help COPA examine its own outcomes for potential bias, and it could assist journalists, activists, and members of the public who are seeking insight into how the police accountability infrastructure in Chicago operates. 

### Mission

To achieve the outcomes outlined above, we will create a tool which provides a predicted probability of judgment outcomes based on basic attributes of the case, including demographic attributes of the complainant, the type of the complaint, and demographic attributes of the officers included on the complaint. The model driving this tool will be built using the [COPA Cases dataset](https://data.cityofchicago.org/Public-Safety/COPA-Cases-Summary/mft5-nfa8) from the [Chicago Data Portal](https://data.cityofchicago.org/). The final model must be highly explainable (since the primary audiences for its output are nontechnical and the goal is transparency), so logistic regression and tree-based models will be favored (tree-based methods are also most analytically appropriate since all the predictors are categorical.)

### Success Criteria

We will have three primary success criteria:

- **Model performance**: At this point, we do not have an a priori reason to weight false negatives or false positives differently, so we will plan to use overall accuracy as our model evaluation criterion. However, if we investigate the data and see significant class imbalances which would make accuracy an unreliable indicator, we may have to re-evaluate this. Our baseline goal is to surpass the accuracy of a fully-random model (i.e., do better than just predicting the majority class for all cases.) Once we investigate the data further we may be able to refine this target; however, since the goal is mostly about transparency, we think that if models are not achieving very impressive accuracy we can report this in detail in our public-facing tool, and that will still provide value. 

- **Business value**: The "business" value of this project would be provided if it is deemed a useful tool for COPA, journalists, activists, or the public. Therefore, a long-term goal would be seeing this tool cited in a news article or cited in a context like a city council hearing related to the performance of COPA.

- **User-friendliness**: To achieve the "business" goals of this project, this tool must be very easy to use and interpret for nontechnical audiences (and since we are unlikely to achieve the business goals, this can perhaps serve as a proxy for likeliness to be adopted). Therefore, this tool must adhere very strongly to the (i.e., pass all criteria of) [Nielsen usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) and be simple and intuitive to use. The user should be able to select different combinations of characteristics for a case and see the probability of each possible case outcome for that combination of characteristics, and they should be able to do so without any explanation or training which is not immediately available within the tool's user interface. 

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

# MID PROJECT PR 
## Overall structure:
Step by step details are provided below, but at a high level there are two main locations to edit if you want to change setup for the data acquisition and database creation steps:
* Configuration (S3 Bucket location and S3 key name, local vs. RDS database creation, etc.) for the data acquisition and database creation is stored in /src/config.py.
* For Docker, environment variables (RDS/MYSQL and S3 credentials) should be created in a .env file in the /src directory. This file will be ignored by Git.

## Running data acquisition and database creation locally
### 1. Acquire the data

### Set your S3 credentials

Set environment variables:
* AWS_ACCESS_KEY_ID = < your AWS access key - for instructions on how to find this, see [here](https://aws.amazon.com/blogs/security/how-to-find-update-access-keys-password-mfa-aws-management-console/) >
* AWS_SECRET_ACCESS_KEY = < your AWS secret access key - for instructions on how to find this, see [here](https://aws.amazon.com/blogs/security/how-to-find-update-access-keys-password-mfa-aws-management-console/) >

Or, when running locally, having a ~./aws/credentials file with the above information will also work.

To acquire the data and upload it in S3, configure the desired data URL, S3 bucket name, and S3 key (the way the data will be labeled in the S3 bucket) in config.py. The default values will download the [COPA data](https://data.cityofchicago.org/Public-Safety/COPA-Cases-Summary/mft5-nfa8) and place it in Laurie's "merrell-copa-cases" bucket with the key "copa_raw_data".

To run the acquisition/S3 upload code with the configured values, navigate into the /src directory and run:

`python acquire_copa_data.py`

**NOTE: This script (when using the default URL) downloads a full file from the Chicago Data Portal. It does not do an API call, it downloads a full CSV of 80k+ rows. PLEASE DO NOT RUN THIS COMMAND REPEATEDLY WITH THE DEFAULT URL, TO AVOID OVERTAXING THE DATA PORTAL SITE. If you want to test the call, please change the URL in /src/config.py to "https://raw.githubusercontent.com/lauriemerrell/dummy_data/master/dummy_data.txt" - this contains a dummy text file which you can download as much as you want.**

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

This command builds the Docker image, with the tag `copa`, based on the instructions in `src/Dockerfile` and the files existing in this directory.
 
#### 2. Run the container 

To run the data acquisition code, run from root: 

```bash
docker run --env-file ./src/config.env copa
```
**NOTE: This script (when using the default URL) downloads a full file from the Chicago Data Portal. It does not do an API call, it downloads a full CSV of 80k+ rows. PLEASE DO NOT RUN THIS COMMAND REPEATEDLY WITH THE DEFAULT URL, TO AVOID OVERTAXING THE DATA PORTAL SITE. If you want to test the call, please change the URL in /src/config.py to "https://raw.githubusercontent.com/lauriemerrell/dummy_data/master/dummy_data.txt" and rebuild your Docker image - the new URL contains a dummy text file which you can download as much as you want.**

### 3. Kill the container 

Once finished, you will need to kill the container. To do so: 

```bash
docker kill copa 
```