# MSiA423 Template Repository

<!-- toc -->

- [Project charter](#project-charter)
    * [Vision](#vision)
    * [Mission](#mission)
    * [Success criteria](#success-criteria)
- [Project backlog](#project-backlog)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)

<!-- tocstop -->

# Chicago Civilian Office of Police Accountability Case Outcome Prediction Project

**Developer**: Laurie Merrell

**QA**: Joe Baka

##Project charter

### Vision

Accountability is an important component of the relationship between police departments and the communities in which they operate. One important aspect of this accountability is provided by oversight boards which hear complaints of alleged misconduct by police officers and provide rulings on the merits of these complaints (whether or not they are justified). In Chicago, the Civilian Office of Police Accountability ([COPA](https://www.chicagocopa.org/)) serves this function by hearing cases and deciding whether misconduct occurred (for more information, see COPA's [reference page on the investigative process](https://www.chicagocopa.org/investigations/investigative-process/)). For the public in Chicago to have additional oversight of this process, particularly in the current climate of fraught relationships between police departments and many communities (especially Black communities), it would be useful to have insight on whether complainants of certain races or certain ages are more or less likely to receive favorable outcomes in their complaints than others. This information could help COPA examine its own outcomes for potential bias, and it could assist journalists, activists, and members of the public who are seeking insight into how the police accountability infrastructure in Chicago operates. 

### Mission

To achieve the outcomes outlined above, we will create a tool which provides a predicted probability of judgment outcomes based on basic attributes of the case, including demographic attributes of the complainant, the type of the complaint, and demographic attributes of the officers included on the complaint. The model driving this tool will be built using the [COPA Cases dataset](https://data.cityofchicago.org/Public-Safety/COPA-Cases-Summary/mft5-nfa8) from the [Chicago Data Portal](https://data.cityofchicago.org/). The final model must be highly explainable (since the primary audiences for its output are nontechnical and the goal is transparency), so logistic regression and tree-based models will be favored (tree-based methods are also most analytically appropriate since all the predictors are categorical.)

### Success Criteria

We will have three primary success criteria:

- **Model performance**: At this point, we do not have an a priori reason to weight false negatives or false positives differently, so we will plan to use overall accuracy as our model evaluation criterion. However, if we investigate the data and see significant class imbalances which would make accuracy an unreliable indicator, we may have to re-evaluate this. Our baseline goal is to surpass the accuracy of a fully-random model (i.e., do better than just predicting the majority class for all cases.) Once we investigate the data further we may be able to refine this target; however, since the goal is mostly about transparency, we think that if models are not achieving very impressive accuracy we can report this in detail in our public-facing tool, and that will still provide value. 

- **Business value**: The "business" value of this project would be provided if it is deemed a useful tool for COPA, journalists, activists, or the public. Therefore, a long-term goal would be seeing this tool cited in a news article or cited in a context like a city council hearing related to the performance of COPA.

- **User-friendliness**: To achieve the "business" goals of this project, this tool must be very easy to use and interpret for nontechnical audiences (and since we are unlikely to achieve the business goals, this can perhaps serve as a proxy for likeliness to be adopted). Therefore, this tool must adhere very strongly to the (i.e., pass all criteria of) [Nielsen usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) and be simple and intuitive to use.

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

## Running the app
### 1. Initialize the database 

#### Create the database with a single song 
To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create_db --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db` with the initial song *Radar* by Britney spears. 
#### Adding additional songs 
To add an additional song:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.