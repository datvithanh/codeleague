import pandas as pd
import numpy as np
from datetime import datetime

def check_interval(interval):
    distinct_users = set([tmp[2] for tmp in interval])
    concentrate_rate = len(interval)/len(distinct_users)
    if concentrate_rate >= 3.0:
        users = [tmp[2] for tmp in interval]
        user_di = {}
        for u in users:
            if u in user_di.keys():
                user_di[u] +=1
            else:
                user_di[u] = 1
        
        suspicious_users = []
        max_order_propotion = 0
        for k, v in user_di.items():
            if v > max_order_propotion:
                max_order_propotion = v
                suspicious_users = [k]
            else:
                if v == max_order_propotion:
                    suspicious_users.append(k)
                else:
                    pass
        return suspicious_users
    else:
        return []

def str2timestamp(s):
    timeobj = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    return datetime.timestamp(timeobj)

def check_brushing(shop_records, shopid):
    shop_records = sorted(shop_records, key=lambda x: str2timestamp(x[-1]))
    suspicious_users = []
    for i in range(len(shop_records)):
        interval = [shop_records[i]]
        starttime = str2timestamp(shop_records[i][-1])
        for j in range(i+1, len(shop_records)):
            curtime = str2timestamp(shop_records[j][-1])
            if curtime - starttime < 3600:
                interval.append(shop_records[j])

        suspicious_users = suspicious_users + check_interval(interval)

    if len(suspicious_users) > 0:
        with open(f'shops/{shopid}.txt', 'w+') as f:
            for i in set(suspicious_users):
                f.write(f'{shopid},{i}\n')
        

