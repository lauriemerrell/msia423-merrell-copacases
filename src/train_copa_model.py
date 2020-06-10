import pandas as pd
import logging
import s3fs
import pickle

from sklearn import model_selection
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingClassifier

logger = logging.getLogger('train_model')

def train_copa_model(clean_loc, features, target, split_random_state, test_size,
                     model_loc, fit_random_state,ov_acc_loc, acc_loc, prev_loc, var_loc, app_loc, app_flag):
    """
    Train model and save out artifacts and all combinations of input variables, which can be used to create database for app.
    Args:

        clean_loc(str): Filepath to data.
        features (list of strings): List of columns to include as features for training.
        target (str): Name of target (response) column.
        split_random_state (int): Random state seed for train/test.
        test_size (float): Proportion of data to hold out as test set.
        model_loc (str): Filepath to save trained model object.
        fit_random_state (int): Random state for model fitting.
        ov_acc_loc (str): Filepath to save overall accuracy.
        acc_loc (str): Filepath to save information about model accuracy by class.
        prev_loc (str): Filepath to save information about class prevalence.
        var_loc (str): Filepath to save information about variable importance in the model.
        app_loc (str): Filepath to save all combinations of input features with their predicted responses.
        app_flag (Bool): Flag for whether to generate all unique combinations of input data, which can then be saved to database for use in app.

    Returns:
        None.
    """

    X_train, X_test, y_train, y_test = train_test_split(clean_loc, features, target,
                                                        split_random_state, test_size)
    X_train_enc, X_test_enc, xenc = encode_data(X_train, X_test)

    gb_model = fit_model(X_train_enc, y_train, fit_random_state)

    with open(model_loc, "wb") as f:
        pickle.dump(gb_model,f)
        f.close()

    model_accuracy(X_test_enc, y_test, gb_model, xenc, features, ov_acc_loc, acc_loc, prev_loc, var_loc)
    if app_flag:
        unique_data_combinations(X_train, gb_model, xenc, app_loc)


def train_test_split(clean_loc, features, target, random_state, test_size):
    """
    Split data into train and test sets.
    Args:
        clean_loc(str): Filepath to data.
        features (list of strings): List of columns to include as features for training.
        target (str): Name of target (response) column.
        random_state (int): Random state seed for train/test.
        test_size (float): Proportion of data to hold out as test set.

    Returns:
        X_train, X_test, y_train, y_test dataframes/arrays of split data - X dataframes are features, y are response variables.
    """
    try:
        data = pd.read_csv(clean_loc)
        X_train, X_test, y_train, y_test = model_selection.train_test_split(data[features],
                                                                            data[target], random_state=random_state,
                                                                            test_size=test_size)
        logger.info("Data split into train/test")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logger.error(e)

def encode_data(X_train, X_test):
    """
    One-hot encode features.
    Args:
        X_train (dataframe): Train dataframe (all categorical features).
        X_test (dataframe): Test dataframe (all categorical features).

    Returns:
        X_train, X_test, xenc - dataframes are now one-hot encoded, xenc is the encoder object.
    """
    try:
        #encode feature variables
        xenc = OneHotEncoder(sparse=False, handle_unknown='ignore')
        xenc.fit(X_train)
        X_train_enc = pd.DataFrame(xenc.transform(X_train))
        X_test_enc = pd.DataFrame(xenc.transform(X_test))
        logger.info("Data encoded")
        return X_train_enc, X_test_enc, xenc
    except Exception as e:
        logger.error(e)


def fit_model(X_train_enc, y_train, random_state):
    """
    Fit a GradientBoostingClassifier model.
    Args:
        X_train (dataframe): Input data (features only).
        y_train (1d array): Target variable.
        random_state (int): Random state for model fitting.

    Returns:
        Trained model object.
    """
    try:
        # fit model
        gb = GradientBoostingClassifier(random_state=random_state)
        gb_model = gb.fit(X_train_enc, y_train)
        logger.info("Model fit")
        return gb_model
    except Exception as e:
        logger.error(e)

def model_accuracy(X_test_enc, y_test, model, enc, features, ov_acc_loc, acc_loc, prev_loc, var_loc):
    """
    Calculate accuracy on test set and accuracy by category on test set.
    Args:
        X_test_enc (dataframe or array): One-hot encoded data for the feature test set.
        y_test (series, dataframe, or 1d array): Response variable values for test set. Should not be encoded.
        model (trained model object): Previously trained model.
        enc (Encoder): Sklearn encoder trained on the training data.
        features (list): List of column names for the training data.
        ov_acc_loc (str): Filepath to save overall accuracy.
        acc_loc (str): Filepath to save information about model accuracy by class.
        prev_loc (str): Filepath to save information about class prevalence.
        var_loc (str): Filepath to save information about variable importance in the model.

    Returns:
        None.
    """
    try:
        #make a DF with outcomes and whether they were correct
        pred_y_test = model.predict(X_test_enc)
        acc = pd.DataFrame({"True": y_test, "Predicted": pred_y_test})
        acc["Correct"] = acc["True"] == acc["Predicted"]
        overall_acc = len(acc[acc["Correct"] == True]) / len(acc)
        with open(ov_acc_loc, "w") as f:
            f.write("Accuracy:" + str(overall_acc))
            f.close
        logger.info("Overall accuracy saved to {}".format(ov_acc_loc))

        # get prevalence of each category
        group_prevalence = acc.groupby(["True"], as_index=False).count()
        total = sum(group_prevalence["Correct"])
        group_prevalence["Percent of total"] = group_prevalence["Correct"] / total
        group_prevalence.to_csv(prev_loc)
        logger.info("Group prevalence saved to {}".format(prev_loc))

        # get accuracy by category
        # get percent by group: https://stackoverflow.com/questions/23377108/pandas-percentage-of-total-with-groupby
        acc = acc.groupby(["True", "Correct"]).count().groupby("True").apply(lambda x: 100 * x / float(x.sum()))
        acc.to_csv(acc_loc)
        logger.info("Accuracy by group saved to {}".format(acc_loc))

        # variable importance: https://stackoverflow.com/questions/39043326/computing-feature-importance-with-onehotencoded-features
        variable_importances = pd.DataFrame(model.feature_importances_, index = enc.get_feature_names(features)).sort_values(by = 0, ascending = False)
        variable_importances.to_csv(var_loc)
        logger.info("Variable importance saved to {}".format(var_loc))
    except Exception as e:
        logger.error("Problem in model accuracy evaluation")
        logger.error(e)

def unique_data_combinations(X_train, model, enc, app_loc):
    """
    Create a table of all possible data combinations and their associated predicted probabilities.
    Args:
        X_train (dataframe): Dataset from which unique combinations are to be taken.
        model (trained mode object): Trained model object to predict classes.
        enc (Encoder): OneHotEncoder trained on training dataset.
        app_loc (str): Filepath to save all combinations of input features with their predicted responses.

    Returns:
        None.
    """
    try:
        # generated a dataframe with all combinations of predictors
        # approach from: https://stackoverflow.com/questions/53699012/performant-cartesian-product-cross-join-with-pandas
        unique_data = pd.DataFrame()
        for col in X_train.columns:
            col_df = pd.DataFrame({col: X_train[col].unique()})
            col_df['key'] = 1
            logger.debug("Processing {}".format(col))
            if len(unique_data) == 0:
                unique_data = unique_data.append(col_df)
            else:
                unique_data = unique_data.merge(col_df, on="key")
        unique_data.drop(columns = "key", inplace = True)
        logger.info("Unique features dataset created")
        # encode the data
        logger.debug("Encoding unique data")
        unique_data_enc = enc.transform(unique_data)
        logger.debug("Generating predictions")
        # generate predictions
        unique_data["pred"] = model.predict(unique_data_enc)
        logger.info("Predictions generated")
        logger.warning("Writing unique-combination data to file - this step takes several minutes to complete")
        # save data
        unique_data.to_csv(app_loc, index=False)
        logger.info('Data written to file in {}'.format(app_loc))
    except Exception as e:
        logger.error(e)




