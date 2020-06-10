import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from src.create_copa_db import COPA_Case_Attributes
from flask_sqlalchemy import SQLAlchemy


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])

# Initialize the database
db = SQLAlchemy(app)

@app.route('/')
def index():
    """Main view with one example row.

    Create view into index page that uses data queried from COPA_Case_Attributes database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        cases = db.session.query(COPA_Case_Attributes).limit(5).all()
        logger.debug("Index page accessed")
        messages = ["Showing: Example predictions"]
        return render_template('index.html', cases=cases, messages=messages)
    except:
        traceback.print_exc()
        logger.warning("Not able to display index, error page returned")
        return render_template('error.html')


@app.route('/search', methods=['GET','POST'])
def search_for_outcome():
    """View that process a POST with new song input

    :return: redirect to index page
    """
    try:
        # matching input to variable: https://stackoverflow.com/questions/14105452/what-is-the-cause-of-the-bad-request-error-when-submitting-form-in-flask-applica
        req = request.form
        print(req)
        query = db.session.query(COPA_Case_Attributes)
        logger.info("Query initialized")
        field_list = ["police_shooting", "race_complainants", "sex_complainants", "age_complainants",
                    "race_officers","sex_involved_officers", "age_officers", "excessive_force",
                    "years_on_force_officers"]
        field_label = {"police_shooting":"Police shooting: ", "race_complainants":"Race of complainant: ", "sex_complainants": "Gender of complainant: ",
                       "age_complainants": "Age of complainant: ",
                      "race_officers": "Race of officer: ", "sex_involved_officers": "Gender of officer: ",
                       "age_officers": "Age of officer: ", "excessive_force": "Excessive force: ",
                      "years_on_force_officers": "Years on force of officer: "}
        messages = ["Showing: Predictions displayed based on selection - "]
        detail = ""
        # build query dynamically: https://stackoverflow.com/questions/37336520/sqlalchemy-dynamic-filter
        # build query dynamically: https://stackoverflow.com/questions/7604967/sqlalchemy-build-query-filter-dynamically-from-dict
        # get query attr rather than string: https://stackoverflow.com/questions/10251724/how-to-give-column-name-dynamically-from-string-variable-in-sql-alchemy-filter
        for f in field_list:
            if request.form[f]:
                query = query.filter(getattr(COPA_Case_Attributes, f) == request.form[f])
                detail = detail+field_label[f]+request.form[f]+". "
        if detail == "":
            detail = "None"
        logger.info("Perform query")
        cases = query.limit(app.config["MAX_ROWS"]).all()
        logger.info("Query results: {}".format(cases))
        messages.append(detail)
        return render_template('index.html', cases=cases, messages = messages)
    except Exception as e:
        logger.error(e)
        logger.warning("Not able to display search, error page returned")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])