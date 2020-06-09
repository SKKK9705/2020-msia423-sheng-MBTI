import pandas as pd
import yaml
import logging
import sklearn
from sklearn import model_selection
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
import pickle


logging.basicConfig(level=logging.DEBUG, format='%(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger()

methods = dict(logistic_regression = linear_model.LogisticRegression,
               random_forest = RandomForestClassifier,
               decision_tree = DecisionTreeClassifier)


def split_data(path=None, features = None, targets = None, test_size=None, random_state=None, **kwargs):
    """split data to train set and test set

    :param path: path to retrieve model_data.csv
    :param features: feature columns
    :param targets: target columns
    :param test_size: percentage of data to be testset
    :param random_state: a number to ensure same splitting results
    :return: datasets after split
    """

    # read in preprocessed data and seperate by features and target variables
    model_data = pd.read_csv(path)
    features = model_data[features]
    targets = model_data[targets]

    # split data using random state
    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        features, targets, test_size=test_size, random_state=random_state)

    # four target classifiers
    y_train_IE = y_train['I-E']
    y_train_NS = y_train['N-S']
    y_train_TF = y_train['T-F']
    y_train_JP = y_train['J-P']

    y_test_IE = y_test['I-E']
    y_test_NS = y_test['N-S']
    y_test_TF = y_test['T-F']
    y_test_JP = y_test['J-P']

    logger.info('train and test splitted with test size of %s', test_size)
    logger.warning('response variable y is divided into four classifiers, so you will see four y_train and four y_test.')
    return X_train, X_test, y_train_IE, y_train_NS, y_train_TF, y_train_JP, y_test_IE, y_test_NS, y_test_TF, y_test_JP


def train(X_train, y_train, method=None, **kwargs):
    """ train the model using three different methods

    :param X_train: x_train dataset
    :param y_train: y_train dataset
    :param method: three options: logistic regression, random forest and decision tree
    :return: trained model
    """
    assert method in methods.keys()
    logger.info('%s method fitted', method)

    if method == 'logistic_regression':
        # set up logistic regression model
        lr = linear_model.LogisticRegression(fit_intercept=False, penalty='l1')
        # fit that with train datasets
        lr.fit(X_train, y_train)
        logger.info('logistic regression model fitted.')
        return lr

    elif method == 'random_forest':
        # set up random forest model
        rf = RandomForestClassifier(random_state=42)
        # fit that with train datasets
        rf.fit(X_train, y_train)
        logger.info('random forest fitted')
        return rf

    elif method == 'decision_tree':
        # set up decision tree model
        dt = DecisionTreeClassifier(random_state=42)
        # fit that with train datasets
        dt.fit(X_train, y_train)
        logger.info('decision tree fitted')
        return dt


def run_train(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f)

    X_train, X_test, y_train_IE, y_train_NS, y_train_TF, y_train_JP, y_test_IE, y_test_NS, y_test_TF, y_test_JP = split_data(**config['train_model']['split_data'])

    train_model_IE = train(X_train, y_train_IE, **config['train_model']['train'])
    train_model_NS = train(X_train, y_train_NS, **config['train_model']['train'])
    train_model_TF = train(X_train, y_train_TF, **config['train_model']['train'])
    train_model_JP = train(X_train, y_train_JP, **config['train_model']['train'])

    # save datasets yo csv files
    X_test.to_csv(args.xtestpath, index=False)
    y_test_IE.to_csv(args.ytestpathie, index=False, header=False)
    y_test_NS.to_csv(args.ytestpathns, index=False, header=False)
    y_test_TF.to_csv(args.ytestpathtf, index=False, header=False)
    y_test_JP.to_csv(args.ytestpathjp, index=False, header=False)
    logger.info('test sets saved under data folder as xtest.csv, ytestie.csv, ytestns.csv, ytesttf.csv and ytestjp.csv')

    # save pretrained models
    with open(args.modelpathie, "wb") as f:
        pickle.dump(train_model_IE, f)
    with open(args.modelpathns, "wb") as f:
        pickle.dump(train_model_NS, f)
    with open(args.modelpathtf, "wb") as f:
        pickle.dump(train_model_TF, f)
    with open(args.modelpathjp, "wb") as f:
        pickle.dump(train_model_JP, f)

    logger.info('models saved to models folder.')
    logger.warning('you will see four models saved because of four classifiers.')
