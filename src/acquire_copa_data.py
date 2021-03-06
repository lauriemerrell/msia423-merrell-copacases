import requests
import boto3
import logging

logger = logging.getLogger('acquire-copa')

def acquire_copa_data(url, s3_bucket, s3_key):
    """Read COPA data score records from URL and upload to S3 Bucket.
    Args:
        url (`str`): URL from which to request data.
        s3_bucket (`str`): Name of S3 bucket in which to store data.
        s3_key (`str`): Name of S3 key to label the data.
    Returns:
        None.
    """
    # request data
    data = pull_copa_data(url)

    # if there was an error, we get None from pull_copa_data - check that this has not occurred
    if data is not None:
        # get S3 bucket and key from configs and upload
        put_in_S3(data, s3_bucket, s3_key)

def pull_copa_data(url):
    """ Pull data from URL.
    Args:
        url (str): URL from which to request data.

    Returns:
        data (str): Unparsed text returned from URL. Returns None if request is unsuccessful.
    """

    # try to pull data from specified URL, catch RequestException (ex. bad URL)
    try:
        # get data - raw_data is a requests object
        raw_data = requests.get(url)

        # check that response is successful
        if raw_data.status_code == 200:
            # extract just the data (unparsed text - COPA data is a CSV)
            data = raw_data.text

            # check that we actually received data - syntax from: https://stackoverflow.com/questions/47778372/python-requests-fail-silently
            if data:
                data_len = len(data.split("\n"))
                logger.info("Retrieved {} lines of data".format(data_len))
                return data
            # if no data, log error and return none
            else:
                logger.error("No data returned from URL despite successful response code - returning None.")
                return None
        # if bad status code, log an error and return None
        else:
            status = raw_data.status_code
            logger.error("URL data request failed with status {}  - returning None.".format(status))
            return None

    # if exception (request unsuccessful), log error and return none
    except RequestException:
        logger.error("Data request failed. Returning None.")
        return None

def put_in_S3(data, s3_bucket, s3_key):
    """Write a string of data to the specified AWS S3 bucket.

    Args:
        data (str): Raw data to write to S3.
        bucket_name (str): The name of the bucket to which the data will be written. User must have write permissions.
        key (str): S3 Key to apply to the data when it's uploaded.

    Returns:
        None.
    """
    # start s3 resource
    s3 = boto3.resource("s3")

    # try to put the data in the bucket
    try:
        # put the input data in the given bucket with the given key as label
        bucket = s3.Bucket(s3_bucket)
        bucket.put_object(
            Body=data,
            Key=s3_key)
        logger.info("Data successfully placed in {} bucket in S3 with key".format(s3_bucket,s3_key))

    # catch BotoCore exceptions - this includes AWS exceptions (as ClientErrors)
    except Exception as e:
        logger.error("Error: Could not save data in S3.")
        logger.error(e)


