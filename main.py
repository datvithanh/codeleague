import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

from joblib import Parallel, delayed

print('load df')

df = pd.read_csv('logistics-shopee-code-league/delivery_orders_march.csv')
npar = np.array(df)

sla_mat = [[3, 5, 7, 7], [5, 5, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7]]

def timestamp2date(ts):
    dt = datetime.fromtimestamp(ts)
    dt = dt.replace(hour=0, minute=0, second=0)
    return dt

def deststr2idx(s):
    dests = ['Metro Manila', 'Luzon', 'Visayas', 'Mindanao']
    for idx, dest in enumerate(dests):
        if dest.lower() in s.lower():
            return idx
    return False

def get_sla(seller_add, buyer_add):
    seller_idx = deststr2idx(seller_add)
    buyer_idx = deststr2idx(buyer_add)
    return sla_mat[seller_idx][buyer_idx]

# 2020-03-08 (Sunday);
# 2020-03-25 (Wednesday);
# 2020-03-30 (Monday);
# 2020-03-31 (Tuesday);

public_holidays = [datetime.strptime('2020-03-25', '%Y-%m-%d'), 
                  datetime.strptime('2020-03-30', '%Y-%m-%d'), 
                  datetime.strptime('2020-03-31', '%Y-%m-%d')]

def count_holidays(start, end):
    count = 0
    for ph in public_holidays:
        if ph >= start and ph <= end:
            count += 1
    return count

def count_sundays(start, end):
    count = 0
    for i in range(10000):
        date = start + timedelta(days=i)
        if date > end: 
            break
        if date.weekday() == 6:
            count += 1
    return count

def process_order(row):
    sla = get_sla(row[-1], row[-2])
    date_pick = timestamp2date(row[1])
    date_1st_attempt = timestamp2date(row[2])

    if np.isnan(row[3]):
        num_holidays = count_holidays(date_pick, date_1st_attempt)
        num_sundays = count_sundays(date_pick, date_1st_attempt)
        delta = date_1st_attempt - date_pick
        total_days = delta.days - num_holidays - num_sundays
        if total_days <= sla:
            return 0
        
        return 1
    
    date_2st_attempt = timestamp2date(row[3])
    
    if (date_2st_attempt - date_1st_attempt).days > 3:
        return 1
    return 0
#    num_holidays = count_holidays(date_pick, date_2st_attempt)
#    num_sundays = count_sundays(date_pick, date_2st_attempt)
#    delta = date_2st_attempt - date_pick
#    total_days = delta.days - num_holidays - num_sundays
#    if total_days <= sla:
#        return 0
#    
#    return 1

islate = Parallel(n_jobs=12)(delayed(process_order)(row) for row in tqdm(npar))
ids = [tmp[0] for tmp in npar]

with open('submission.csv', 'w+') as f:
    f.write('orderid,is_late\n')
    for k, v in zip(ids, islate):
        f.write(f'{k},{v}\n')
