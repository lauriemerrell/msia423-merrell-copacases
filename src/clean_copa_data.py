import pandas as pd
import logging
import s3fs

logger = logging.getLogger('clean_copa_data')

def clean_copa_data(raw_loc, clean_loc):
    """Read COPA data from location and clean it.
    Args:
        raw_loc (`str`): Location of raw data to be cleaned (expected to be in format compatible with "read_csv").
        clean_loc(`str`): Location to save the cleaned data (CSV).
    Returns:
        None.
    """
    # request data
    data = load_data(raw_loc)

    # clean data
    data = drop_invalid(data)

    # featurize
    data = make_excessive_force(data)

    # put data in S3
    data.to_csv(clean_loc, index=False)
    logger.info('Data written to file in {}'.format(clean_loc))

def load_data(location):
    """
    Args:
        location (`str`): Location of data - CSV format.

    Returns:
        Dataframe of loaded data.
    """
    try:
        logger.debug("Loading data")
        data = pd.read_csv(location)
        logger.info("Dataframe of {} rows successfully loaded from {}".format(len(data),location))
        return data
    except Exception as e:
        logger.error(e)


def drop_invalid(data):
    """
    Drop rows which are not valid for analysis. Keep only COPA/IPRA cases of type "complaint" and status "closed" with single officer + complainant.
    Args:
        data (datafrome): COPA data.

    Returns:
        Cleaned dataframe which can be used for featurization and modeling.
    """
    try:
        data = drop_too_recent(data)
        data = drop_status_asst(data)
        data = drop_nas(data)
        data = drop_multiples(data)
        data = complaints_only(data)
        logger.info("Data clean - {} rows".format(len(data)))
        return data
    except Exception as e:
        logger.error(e)

def drop_too_recent(data):
    """Helper function for drop_invalid - drops rows with date after May 9 2020."""
    data['COMPLAINT_DATE'] = pd.to_datetime(data['COMPLAINT_DATE'], infer_datetime_format=True)
    data = data[data['COMPLAINT_DATE'] < "2020-05-10"]
    return data

def drop_status_asst(data):
    """Helper function for drop_invalid - drops rows with owner other than COPA/IPRA and status other than closed."""
    # keep only closed COPA/IPRA data
    before = len(data)
    data = data[(data['ASSIGNMENT'] != "BIA") & (data['CURRENT_STATUS'] == "Closed")]
    after = len(data)
    logger.info("Dropped {} rows for status and assignment".format(before - after))
    return data

def drop_nas(data):
    """Helper function for drop_invalid - drop rows with missing data."""
    # drop NAs
    before = len(data)
    data = data.dropna(subset=['RACE_OF_COMPLAINANTS', 'SEX_OF_COMPLAINANTS', 'AGE_OF_COMPLAINANTS',
                               'RACE_OF_INVOLVED_OFFICERS', 'SEX_OF_INVOLVED_OFFICERS',
                               'AGE_OF_INVOLVED_OFFICERS', 'YEARS_ON_FORCE_OF_INVOLVED_OFFICERS'])
    after = len(data)
    logger.info("Dropped {} rows for NAs".format(before - after))
    return data

def drop_multiples(data):
    """Helper function for drop_invalid - drop rows with multiple officers or complainants."""
    # drop cases with multiple complainants or multiple officers
    before = len(data)
    # https://stackoverflow.com/questions/27975069/how-to-filter-rows-containing-a-string-pattern-from-a-pandas-dataframe
    data = data[~data['RACE_OF_COMPLAINANTS'].str.contains("\|")]
    data = data[~data['RACE_OF_INVOLVED_OFFICERS'].str.contains("\|")]
    data = data[~data['FINDING_CODE'].str.contains("\|")]
    after = len(data)
    logger.info("Dropped {} rows for multiples".format(before - after))
    return data

def make_excessive_force(data):
    """
    Make an excessive force column in COPA data
    Args:
        data (dataframe): COPA dataset with 'CURRENT_CATEGORY' column.

    Returns:
        Dataframe with EXCESSIVE_FORCE indicator column added.
    """
    try:
        data['EXCESSIVE_FORCE'] = data['CURRENT_CATEGORY'] == "Excessive Force"
        logger.info("Excessive force column created")
        return data
    except Exception as e:
        logger.error(e)

def complaints_only(data):
    """Helper function for drop_invalid - drop rows with non-complaint types."""
    before = len(data)
    data = data[data['CASE_TYPE'] == "Complaint"]
    after = len(data)
    logger.info("Dropped {} rows of non-complaints".format(before - after))
    return data
