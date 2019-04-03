import numpy as np
from evolving import util


def prequential_evaluation(method, data, labels, metric, train_size, window_size=1, fading_factor=1, adjust_labels=0):
    '''
    :param method: clustering method to be evaluated
    :param data: data for training and test
    :param labels: ground truth labels
    :param metric: error metric
    :param train_size: number of samples for the first training step
    :param window_size: window size for each prequential iteration
    :param fading_factor: fading factor for older test samples
    :param adjust_labels: adjust labels given the original index. 0 = no adjust, 1 = adjuts in first training, 2 = adjust during the entire prequential process
    :return:
    accumulated error, error list
    '''

    test_end = 0
    index = 0
    limit = len(labels)
    accumulated_error = 0
    error_list = []

    while test_end < limit:
        train_start, train_end, test_start, test_end = getDataIndex(index, train_size, window_size, limit)
        train_data = data[train_start:train_end]
        test_data = data[test_start:test_end]
        index = test_start

        method.fit(train_data)
        y_hat = method.predict(test_data)
        y = labels[test_start:test_end]

        if adjust_labels == 2 or (index == test_start and adjust_labels == 1):
            y_hat = util.adjust_labels(y_hat, y)

        error = metric(y, y_hat)
        accumulated_error += fading_factor * error
        error_list.append(error)

    return accumulated_error, error_list


def getDataIndex(index, train_size, window_size, limit):

    train_start = index

    if index == 0:
        train_end = index + train_size
    else:
        train_end = index + window_size

    test_start = train_end
    test_end = min(test_start + window_size, limit)

    return train_start, train_end, test_start, test_end
