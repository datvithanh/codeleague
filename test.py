import numpy as np
import pandas as pd
import lightgbm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer


#
# Prepare the data
#

train = pd.read_csv('train.csv')

# get the labels
y = train.column_label.values
# print(train)
train.drop(['id', 'column_label'], inplace=True, axis=1)

x = np.array(train)

#
# Create training and validation sets
#
x, x_test, y, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

#
# Create the LightGBM data containers
#

categorical_features = [c for c, col in enumerate(train.columns) if 'cat' in col]
categorical_features = [2]
print(x)
train_data = lightgbm.Dataset(x, label=y, feature_name=['1', '2', '3', '4'], categorical_feature=['3'])
test_data = lightgbm.Dataset(x_test, label=y_test)

#
# Train the model
#

parameters = {
    'application': 'binary',
    'objective': 'binary',
    'metric': 'auc',
    'is_unbalance': 'true',
    'boosting': 'gbdt',
    'num_leaves': 31,
    'feature_fraction': 0.5,
    'bagging_fraction': 0.5,
    'bagging_freq': 20,
    'learning_rate': 0.05,
    'verbose': 0
}

model = lightgbm.train(parameters,
                       train_data,
                       valid_sets=test_data,
                       num_boost_round=5000,
                       early_stopping_rounds=100)
#
# Create a submission
#

submission = pd.read_csv('test.csv')
ids = submission['id'].values
submission.drop('id', inplace=True, axis=1)


x = submission.values
y = model.predict(x)

output = pd.DataFrame({'id': ids, 'target': y})
output.to_csv("submission.csv", index=False)