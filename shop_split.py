import os

import pandas as pd
import numpy as np
from tqdm import tqdm

from interval import check_brushing
from joblib import Parallel, delayed

df = pd.read_csv('order_brush_order.csv')
shops = {} 
npar = np.array(df)

for row in tqdm(npar):
    if row[1] in shops.keys():
        shops[row[1]].append(row)
    else:
        shops[row[1]] = [row]

Parallel(n_jobs=4)(delayed(check_brushing)(shops[k], k) for k, _ in tqdm(shops.items()))
