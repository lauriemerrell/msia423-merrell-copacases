# MSiA423 Template Repository

<!-- toc -->

- [Project charter](#project-charter)
    * [Vision](#vision)
    * [Mission](#mission)
    * [Success criteria](#success-criteria)
- [Directory structure](#directory-structure)
- [Instructions](#instructions)
  * [How to run the model pipeline](#how-to-run-the-model-pipeline )
  * [How to run the model pipeline with database creation](#how-to-run-the-model-pipeline-with-database-creation)
  * [How to run the actual app](#how-to-run-the-actual-app)
  * [Logging](#logging)
 - [Repo structure](#repo-structure)
 - [References](#references)

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

## Instructions

All commands listed in this section should be run from the root directory. 

### How to run the model pipeline 

Ensure that you have your S3 credentials set as environment variables (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`). Default settings are all specified in config/config.yaml. If you want to run with the default settings (which do NOT include creating or putting data in a MySQL database of any kind), you can run the following two commands from the root directory:

`docker build -f Dockerfile_model -t model .`

followed by

`docker run --mount type=bind,source="$(pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY model  run.py config/config.yaml`

This command (if the default YAML settings are not changed) will: clean and featurize the raw data from S3, put the cleaned data in S3, and then train a model on the clean data from S3. Model output objects will be saved in the models directory if run with default settings. The expected model output objects are:
- model.p pickle file with trained model object
- ov_acc.txt which prints the overall test accuracy (expected value with default settings is: 0.45756880733944955)
- accuracy.csv which prints the test accuracy by true category
- prevalence.csv which prints the true category prevalence in the test data
- var_imp.csv which prints the variable importance in the trained model

You can run with a different YAML file by changing "config/config.yaml" to the desired filepath in the docker run command. You can change the "ACQUIRE_FLAG" in the default YAML to begin the pipeline by downloading from the original data source instead of with the raw data already in S3. 

### How to run the model pipeline with database creation

If you want to generate the data to be placed in the database (all combinations of input variables - it is slow to generate), build the database, and put the data in it, you can modify the config/config.yaml file as follows: change APP_DATA_FLAG to True and DB_FLAG to True. Ensure that your SQLALCHEMY_DATABASE_URI environment variable is set as follows (for RDS): "mysql+pymysql://user:password@host:port" (without quotes - example from Lab 4 documentation.) You must be connected to Northwestern GlobalProtect VPN for this to work if using RDS (as opposed to a local SQLite database.).

Then run the same Docker build command as above, followed by this new run command - this version can take over 40 minutes to complete:
`docker run --mount type=bind,source="$(pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e SQLALCHEMY_DATABASE_URI model run.py config/config.yaml`

This will run all the model fitting steps but will also generate all the data to put in the database (which takes several minutes) and then put it in the database (which takes about 40 minutes).

### How to run the model pipeline unit tests

Run `docker run app -m pytest` (using the Dockerfile built earlier with the name "app").

Unit test results will be printed to console. There are 16 unit tests; most functions write to file so are not unit tested.

### How to run the actual app

To run the web app, ensure that your SQLALCHEMY_DATABASE_URI environment variable is set as follows (for RDS): "mysql+pymysql://user:password@host:port" (without quotes - example from Lab 4 documentation.) You must be connected to Northwestern GlobalProtect VPN for this to work if using RDS (as opposed to a local SQLite database.)

Run `docker build -f Dockerfile_app -t app .` to build the Docker image and then run `docker run --publish 5000:5000 -e SQLALCHEMY_DATABASE_URI app app.py` to run. You can access the app in a browser at http://0.0.0.0:5000/ locally. Users should not set any configuration for the app, but the settings can be reviewed in the config/flaskconfig.py file. You will need to use CTRL+C to quit the app once it's running.

### Logging

Logging settings can be specified in config/logging/local.conf. If you run with default settings you should only get INFO logging alerts from the code in this repo, except that the Flask app logger (werkzeug) will log a warning when you run the app saying that the debugger is active.

## Repo structure
The app/templates directory contains the HTML files for the Flask app. The config directory contains configuration files. The deliverables directory contains the final presentation slides. The models directory is empty but is where the model artifacts are saved by default when the pipeline is run. The notebooks directory contains a Jupyter notebook used for the project. The project management directory contains the project backlog and pull request documentation.  The src directory contains all the scripts for the model pipeline. The test directory contains test scripts and a test dataset which they validate against. 

All files needed to run the pipeline or the app directly are saved in the root directory.

## References
Direct lines of code are cited as comments inline. These inline references are aggregated here (Does not include documentation for packages themselves -- they are implied resources. Requirements.txt has full list of packages needed.) The app UI was built using Bootstrap. References regarding the data itself are in the presentation in the deliverables directory and linked in the app Web UI.

Two references not cited inline about writing model to file:
- https://stackoverflow.com/questions/33054527/typeerror-a-bytes-like-object-is-required-not-str-when-writing-to-a-file-in
- https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/

Model pipeline:
- https://stackoverflow.com/questions/27975069/how-to-filter-rows-containing-a-string-pattern-from-a-pandas-dataframe
- https://stackoverflow.com/questions/53699012/performant-cartesian-product-cross-join-with-pandas
- https://stackoverflow.com/questions/23377108/pandas-percentage-of-total-with-groupby
- https://stackoverflow.com/questions/39043326/computing-feature-importance-with-onehotencoded-features
- https://stackoverflow.com/questions/47778372/python-requests-fail-silently

App:
- https://stackoverflow.com/questions/14105452/what-is-the-cause-of-the-bad-request-error-when-submitting-form-in-flask-applica
- https://stackoverflow.com/questions/37336520/sqlalchemy-dynamic-filter
- https://stackoverflow.com/questions/7604967/sqlalchemy-build-query-filter-dynamically-from-dict
- https://stackoverflow.com/questions/10251724/how-to-give-column-name-dynamically-from-string-variable-in-sql-alchemy-filter
