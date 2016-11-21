import csv
import os
import sys
import time
import numpy as np
from shutil import copyfile
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn import ensemble
from numpy import genfromtxt, savetxt
from sklearn.metrics import mean_squared_error

# get the dataset
# X : feature set get data from PCA_train_scored.csv
# Y : sales price get data from train_scored_y.csv

# ########################### read file populate dataset ########################


def read_dataset(file_name, label_file = False):
    f = open(file_name)
    csv_f = csv.reader(f, delimiter=',')
    csv_f.next()

    if not label_file:
        dataset = [[np.float(value) for value in sample[1:81]] for sample in csv_f]
    else:
        # dataset = [sample for sample in csv_f]
        dataset = [np.float(sample[0]) for sample in csv_f]

    dataset = np.array(dataset)

    return dataset

def get_filtered_dataset(dataset_file, feature_file):
    feature = open(feature_file)
    csv_f = csv.reader(feature, delimiter=',')
    feature_list = [feature_name for feature_name in csv_f]

    data = open(dataset_file)
    csv_f = csv.reader(data, delimiter=',')
    return csv_f

#####################write file populate dataset###############################

def writeOutput(predictedValues, type):

    n = len(predictedValues)
    id = 1460
    filePath = './data/'+ type +'/'+ type+'output.csv'

    if os.path.isfile(filePath):
        copyfile('./data/'+ type +'/'+ type +'output.csv', './data/'+ type +'/'+ type +'output_'+time.ctime()+'.csv')
        os.remove(filePath)

    if sys.version_info[0] > 3:
        out_file = open(filePath, 'w', newline='')
    else:
        out_file = open(filePath, 'w')

    writer = csv.writer(out_file)
    header = ['Id', 'SalePrice']
    writer.writerow(header)

    for i in range(0,n):
        id += 1
        line = [id, predictedValues[i]]
        writer.writerow(line)

    out_file.close()

def adaboost():
    # train = genfromtxt(open('./data/PCA_train_scored.csv', 'r'), delimiter=',', dtype='f8')[1:]
    # house_prices = genfromtxt(open('./data/train_scored_y.csv', 'r'), delimiter=',', dtype='f8')[1:]
    # test_data = genfromtxt(open('./data/PCA_test_scored.csv', 'r'), delimiter=',', dtype='f8')[1:]

    train = genfromtxt(open('./data/train_scored.csv', 'r'), delimiter=',', dtype='f8')[1:]
    house_prices = genfromtxt(open('./data/train_scored_y.csv', 'r'), delimiter=',', dtype='f8')[1:]
    test_data = genfromtxt(open('./data/test_scored.csv', 'r'), delimiter=',', dtype='f8')[1:, 1:83]

    train_data = train[0:1320, 1:82]
    house_prices_data = house_prices[:1320]

    validation_data = train[1320:, 1:82]
    house_prices_validation = house_prices[1320:]

    #test_data = test[0:, 1:82]

    # Fit regression model
    regr_2 = AdaBoostRegressor(DecisionTreeRegressor(max_depth=12), n_estimators=500,
                               loss='square', learning_rate=1)

    regr_2.fit(train_data, house_prices_data)

    #Predict validation
    y_validation = regr_2.predict(validation_data)
    mse = mean_squared_error(house_prices_validation, y_validation)
    print("AdaBoost MSE: %.4f" % mse)

    # Predict
    y_2 = regr_2.predict(test_data)

    writeOutput(y_2, 'AdaBoost')

def gradboost():
    # train = genfromtxt(open('./data/PCA_train_scored.csv', 'r'), delimiter=',', dtype='f8')[1:]
    # house_prices = genfromtxt(open('./data/train_scored_y.csv', 'r'), delimiter=',', dtype='f8')[1:]
    # test = genfromtxt(open('./data/PCA_test_scored.csv', 'r'), delimiter=',', dtype='f8')[1:]

    train = genfromtxt(open('./data/train_scored.csv', 'r'), delimiter=',', dtype='f8')[1:]
    house_prices = genfromtxt(open('./data/train_scored_y.csv', 'r'), delimiter=',', dtype='f8')[1:]
    test_data = genfromtxt(open('./data/test_scored.csv', 'r'), delimiter=',', dtype='f8')[1:, 1:83]

    train_data = train[0:1320, 1:82]
    house_prices_data = house_prices[:1320]

    validation_data = train[1320:, 1:82]
    house_prices_validation = house_prices[1320:]

    # test_data = test[0:, 1:81]

    # Fit regression model
    params = {'n_estimators': 500, 'max_depth': 12, 'learning_rate': 0.01, 'loss': 'ls'}
    regr_1 = ensemble.GradientBoostingRegressor(**params)

    # regr_1.fit(train_data, house_prices)
    regr_1.fit(train_data, house_prices_data)

    # Predict validation
    y_validation = regr_1.predict(validation_data)
    print("GradientBoost MSE: %.4f" % mean_squared_error(house_prices_validation, y_validation))

    # Predict
    y_2 = regr_1.predict(test_data)
    writeOutput(y_2, 'GradientBoost')

if __name__ == '__main__':
    adaboost()
    print "------------------------------------------------"
    #gradboost()