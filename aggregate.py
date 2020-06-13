import os
import pandas as pd

with open('submission.csv', 'w+') as f:
    df = pd.read_csv('order_brush_order.csv')
    shopids = set(list(df['shopid']))

    di = {tmp: 0 for tmp in shopids}
    print(len(shopids))
    for fn in os.listdir('shops'):
        lines = [tmp.strip().split(',')[-1] for tmp in open(os.path.join('shops', fn), 'r').readlines()]
        shopid = fn[:-4]
        di[int(shopid)] = '&'.join(lines)

    f.write('shopid,userid\n')
    for k, v in di.items():
        f.write(f'{k},{v}\n')