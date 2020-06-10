import argparse
import yaml
import logging.config
import s3fs
from config import py_config
from src.acquire_copa_data import acquire_copa_data
from src.clean_copa_data import clean_copa_data
from src.train_copa_model import train_copa_model
from src.create_copa_db import create_copa_db

if __name__ == '__main__':
    # load configs
    # code from YAML interactive example in class
    parser = argparse.ArgumentParser(description="Model pipeline for COPA case predictions")
    parser.add_argument('config', help="Path to YAML file with model settings")

    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # shout out Kris D on slack for the disable existing loggers thing
    logging.config.fileConfig(config["LOGGING_CONFIG"], disable_existing_loggers=False)

    # ACQUIRE DATA IF FLAG IS SET TO DO SO
    acquire_flag = config["ACQUIRE_FLAG"]
    if acquire_flag:
        # get configuration for data acquisition
        url = config["RAW_DATA_LOCATION"]
        s3_bucket = config["S3_BUCKET_NAME"]
        s3_key = config["S3_KEY_NAME"]
        # acquire
        acquire_copa_data(url, s3_bucket, s3_key)

    # CLEAN DATA IF FLAG IS SET TO DO SO
    clean_flag = config["CLEAN_FLAG"]
    if clean_flag:
        # CLEAN
        # get configuration for data cleaning
        raw_loc = config["DATA_TO_CLEAN"]
        clean_loc = config["CLEAN_SAVE_LOCATION"]
        # clean
        clean_copa_data(raw_loc, clean_loc)

    # FIT MODEL IF FLAG IS SET TO DO SO
    model_flag = config["MODEL_FLAG"]
    if model_flag:
    # TRAIN MODEL
        features = config["FEATURES"]
        target = config["TARGET"]
        split_random_state = config["SPLIT_RANDOM_STATE"]
        test_size = config["TEST_SIZE"]
        model_loc = config["MODEL_SAVE_LOCATION"]
        fit_random_state = config["FIT_RANDOM_STATE"]
        ov_acc_loc = config["OV_ACC_SAVE_LOCATION"]
        acc_loc = config["ACC_SAVE_LOCATION"]
        prev_loc = config["PREV_SAVE_LOCATION"]
        var_loc = config["VAR_SAVE_LOCATION"]
        app_flag = config["APP_DATA_FLAG"]
        app_loc = config["APP_SAVE_LOCATION"]
        train_copa_model(clean_loc, features, target, split_random_state, test_size,
                         model_loc, fit_random_state, ov_acc_loc, acc_loc, prev_loc, var_loc, app_loc, app_flag)

    # BUILD DATABSE IF FLAG IS SET TO DO SO
    db_flag = config["DB_FLAG"]
    if db_flag:
        app_loc = config["APP_SAVE_LOCATION"]
        engine_string = py_config.SQLALCHEMY_DATABASE_URI
        create_copa_db(engine_string, app_loc)




