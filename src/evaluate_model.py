import pandas as pd
import yaml
import argparse
import logging
import sklearn
from sklearn import metrics
import numpy as np
import pickle
import sys

logging.basicConfig(level = logging.DEBUG, format = '%(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger()


def evaluate_model(ytestpath, modelpath, xtestpath = None, **kwargs):
    """ evaluate model built with accuracy, AUC and confusion matrix

    :param modelpath: path of model trained earlier
    :param xtestpath: input path of x_test data
    :param ytestpath: input path of y_test data
    :return: auc, confusion matrix and model accuracy
    """

    with open(modelpath, "rb") as f:
        lr = pickle.load(f)

    X_test = pd.read_csv(xtestpath, header = 0)
    y_test = pd.read_csv(ytestpath, header = None)

    ypred_proba_test = lr.predict_proba(X_test)[:, 1]
    ypred_bin_test = lr.predict(X_test)

    # calculate measurement metrics: auc, confusion metrics and accuracy
    auc = sklearn.metrics.roc_auc_score(y_test, ypred_proba_test)
    confusion = sklearn.metrics.confusion_matrix(y_test, ypred_bin_test)
    accuracy = sklearn.metrics.accuracy_score(y_test, ypred_bin_test)
    classification_report = sklearn.metrics.classification_report(y_test, ypred_bin_test)

    logger.info('AUC on test: %0.3f' % auc)
    logger.info('Accuracy on test: %0.3f' % accuracy)
    logger.info(pd.DataFrame(confusion,
                  index=['Actual negative','Actual positive'],
                  columns=['Predicted negative', 'Predicted positive']))

    return auc, confusion, accuracy


def post_process(modelpath, features=None, **kwargs):
    """ Get feature importances/ odd ratios

    :param modelpath: path of model trained earlier
    :param features: feature columns
    :return: a dataframe which stores ranked feature importances and odd ratios
    """
    with open(modelpath, "rb") as f:
        lr = pickle.load(f)

    fitted = pd.DataFrame(index=features)
    # coefficients / feature importance of each variable
    fitted['coefs'] = lr.coef_[0]
    # odds ratios
    fitted['odds_ratio'] = fitted.coefs.apply(np.exp)
    fitted = fitted.sort_values(by='odds_ratio', ascending=False)

    return fitted


def run_evaluate(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f)

    four = ['ie','ns','jp','tf']
    # write the results to a txt file
    with open(args.output, 'w') as t:
        sys.stdout = t
        for f in four:
            auc, confusion, accuracy = evaluate_model('data/ytest'+f+'.csv', 'models/model'+f+'.pkl', **config['evaluate_model']['evaluate_model'])

            print('AUC for ' + f + ' is:')
            print(auc)
            print()
            print('confusion matrix for ' + f + ' is:')
            print(pd.DataFrame(confusion,
                  index=['Actual negative','Actual positive'],
                  columns=['Predicted negative', 'Predicted positive']))
            print()
            print('accuracy for ' + f + ' is:')
            print(accuracy)
            print()
            print()
            logger.info('model evaluations saved to %s', args.output)

            fitted = post_process('models/model'+f+'.pkl', **config['evaluate_model']['post_process'])
            fitted.to_csv(str(args.outputpost) + '/' + f, index=True)
            logger.info('Feature importances/odd ratios saved to %s', args.outputpost)
