# Project backlog

## Backlog 

Note: I use Fibonacci hour assignments for my task sizes. Task sizes >= 5 should be broken down later. ? indicates that more information is needed to size the task. Story sizes are indicated in parentheses at the end of the story description.

Tasks marked with an asterisk are considered "current" and should be completed within the next two weeks.

- Initiative: App content: Develop models to predict outcomes of COPA cases.
    * Epic: Deliver data for model development. (Note: I chose to break this out as its own epic because I do think providing cleaned/usable data is a discrete deliverable with business value in this case.)
        + *Read data definitions and contextual material (2)
        + *Define subset of data to be used (date range, statuses to include/exclude, etc.) (1)
        + *Exploratory analysis: Investigate distributions of values for each variable (2)
        + *Data cleaning: Handle cases with multiple values per field (2)
        + *Data cleaning: Investigate duplicates or other data integrity issues (2)
        + *Split into train/test sets (<1)
    * Epic: Deliver a final model which meets the accuracy criteria. Note: Since we have a relatively small number of variables, are focused on "simpler" models for explainability purposes, and the data will be cleaned prior to beginning these tasks, I am not estimating that the model fitting will actually take particularly long.
        + *Fit logistic regression model (includes variable selection) (2)
        + *Fit random forest model (2)
        + *Fit boosted tree model (2)
        + *Fit CART model (2)
        + *Compare performance of the different fitted models (logistic, RF, boosted trees, CART) on test set (2)
        + *Investigate variable importance in the different models (1)
        + *Select final model (<1)
        + Model reproducibility work (?)
- Initiative: App infrastructure: Build the pipeline to deploy a model and necessary data to a public-facing app, and the diagnostic tests to ensure continued app performance.
    * Epic: Deliver an S3 bucket for the source data.
    * Epic: Deliver an RDS table to serve data to user interface.
    * Epic (?): Deliver a reproducible pipeline (i.e., address reproducibility - not sure if this a separate epic or should be included within S3, RDS epics.)
        + Connection between Flask app and S3 bucket (?)
        + Connection between Flask app and RDS table (?)
        + Configuration files (?)
    * Epic: Deliver unit tests to ensure stability of application.
- Initiative: App experience: Build a user interface for a public app to display model information and outcomes. 
    * Epic: Deliver Flask app for user to interact with model.
        + Docker setup (?)
        + User interface: User selection of inputs (?)
        + User interface: Display of model results (probability and variable importance) based on user selection (?)

### Icebox 
- App experience
    * Flask app
        + User interface: Display probabilities based on selections left blank (ex. display part of tree structure with different outcomes for values left blank by user) (?)
        + User interface: Display a selection of actual cases from the data which match the characteristics selected by the user 