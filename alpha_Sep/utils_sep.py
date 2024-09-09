## 优化函数  九月

import pandas as pd
import numpy as np
from tqdm import tqdm
tqdm.pandas()


def rsrs(price_stock, window = 15):
    '''
    尝试在rolling过程中使用两列元素, 运行速度有点慢....
    '''
    main_index = price_stock.index[window:]
    sub_index = np.arange(window)
    mul_index = pd.MultiIndex.from_product(
        [main_index, sub_index],
        names=['main_index', 'sub_index']
    )

    res = pd.DataFrame(
        [price_stock.loc[:date].iloc[-window:].values[i] for date in main_index for i in sub_index],
        index=mul_index,
        columns=price_stock.columns
    )

    def utils(data):
        if (data == 1).sum().sum() == 2*window:
            return np.nan
        else:
            return np.polyfit(data.iloc[:, 0], data.iloc[:, 1], 1)[0]
        
    return res.groupby(level='main_index').apply(utils)


def rsrs_v2(price:pd.DataFrame, window=15):
    '''
    直接用for循环计算  速度也有点小慢
    '''
    def _rsrs(price_stock):
        res = pd.Series(index=price_stock.index[window:])
        for i in range(window, len(res)):
            # data = price_stock.iloc[i-window:i, :].fillna(1)
            # res.iloc[i] = np.polyfit(data.xs('adjlow', level='Type', axis=1).values.flatten(), data.xs('adjhigh', level='Type', axis=1).values.flatten(), 1)[0]
            res.iloc[i] = np.polyfit(price_stock.iloc[i-window:i, 0].fillna(1), price_stock.iloc[i-window:i, 1].fillna(1), 1)[0]
        
        return res
            
    return price.groupby('Stock', axis=1).progress_apply(_rsrs)


def rsrs_v3(data, window=15):
    '''
    data是一个每个元素为元组的Series对象
    结果无法运行, apply函数对元素非数值的对象使用
    '''
    data = np.array(data.values.tolist())
    data = np.nan_to_num(data, nan=1)
    if np.sum([data == 1]) == 2 * window:
        return np.nan
    else:
        data += np.random.rand(window, 2) * 1e-6
        return np.polyfit(data[:, 0], data[:, 1], 1)[0]
    
def destop(factor:pd.DataFrame):
    '''
    去掉一字板涨跌停因子
    '''
    is_trading = pd.read_csv('/mnt/datadisk2/aglv/aglv/lab_aglv/is_trading.csv')
    is_trading.index = [str(i) for i in is_trading.index]

    factor.index = [str(i) for i in factor.index]
    res = factor.shift(1) * is_trading.loc[factor.index, factor.columns]
    res.index.names = ['Date']
    return res

def main():
    pass

if __name__ == '__main__':
    main()