'''
主函数：得到策略下组合价值变化
author: 张宇萌
'''
import pandas as pd
import sys
import numpy as np
from statsmodels.formula.api import quantreg
from sympy import symbols, Eq, solve


from VaR import get_diff_VaR,get_VaR,solve_w,get_diff_VaR_stk
from frequency import frequency_cut


import math

#%%
path_data = 'data/data.csv'
path_vol = 'data/vol.csv'
path_idx = 'data/index.csv'

sys.path.insert(0,'.')
data = pd.read_csv(path_data)
vol = pd.read_csv(path_vol)
index = pd.read_csv(path_idx)

#%%
# 裁剪data, vol, index

freq = 1  # 调仓频率 1个月
back = 6  # 回望期/调仓频率 6倍 即6个月
returnset, volset, indexset = frequency_cut(data, vol, index, freq)
rou = [0.334827, 0.434386, 0.540143]

#%%

w = [1/3,1/3,1/3] # 初始 在第一个freq时设为等权重
money = [4000.00,4000.00,4000.00] # 相应地每一种资产分配的资金
quantiles = [.01, .1, .4, .5, .6, .75, .9]
# quantiles = [.005, .1, .25, .5, .75, .975]
# quantiles = [.1, .3, .5, .7, .9]
C = .95  # 置信水平

# 存储asset的价值变化
asset_all = []
asset_all.clear()

for i in range(len(returnset)):

    print(i)

    # 下一个调仓周期
    print(returnset[i])
    return0 = returnset[i].reset_index(drop=True)
    vol0 = volset[i].reset_index(drop=True)
    index0 = indexset[i].reset_index(drop=True)

    # 从超过回望期开始投入资金
    if(i>=back):

        # 回望期
        if(back!=1):
            return_past = pd.concat(returnset[(i-back):(i-1)])
            vol_past = pd.concat(volset[(i-back):(i-1)])
            index_past = pd.concat(indexset[(i-back):(i-1)])
        if(back==1):
            return_past = returnset[i-1]
            vol_past = volset[i-1]
            index_past = indexset[i-1]

        # 原来的计算w方法
        # diff_VaR_1,diff_VaR_2,diff_VaR_3 = get_diff_VaR(return_past,vol_past,w,.01,quantiles,C)
        # w1,w2,w3 = solve_w(diff_VaR_1,diff_VaR_2,diff_VaR_3)

        # 现在的计算w方法
        diff_VaR_1, diff_VaR_2, diff_VaR_3 = get_diff_VaR_stk(return_past, vol_past, ['bank','defense','food'],'std',quantiles,C,w,rou)
        w1, w2, w3 = solve_w(diff_VaR_1, diff_VaR_2, diff_VaR_3)

        # 权重固定
        # w1, w2, w3 = 0.1, 0.6, 0.3
        # w1,w2,w3 = 1/3,1/3,1/3

        w = [w1,w2,w3]
        print(w)


        # 在一个调仓周期开始时 首先根据上面计算得到的w来重新调仓 重新进行资金的配比

        money_sum = money[0]+money[1]+money[2]
        money[0]=money_sum*w1
        money[1]=money_sum*w2
        money[2]=money_sum*w3
        asset_all.append(money_sum)

        # 然后每天根据指数来更新组合的价值 加入asset_all 表示asset价值的变化

        for j in range(len(index0)-1):

            bank1 = index0['bank'][j]
            bank2 = index0['bank'][j+1]

            defense1 = index0['defense'][j]
            defense2 = index0['defense'][j+1]

            food1 = index0['food'][j]
            food2 = index0['food'][j+1]

            money[0] = money[0]/bank1*bank2
            money[1] = money[1]/defense1*defense2
            money[2] = money[2]/food1*food2

            money_sum = money[0]+money[1]+money[2]
            asset_all.append(money_sum)


       
from pandas.core.frame import DataFrame
result = [asset_all]
result = DataFrame(result)
result.to_csv("result.csv")
