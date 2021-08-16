'''
计算各资产的VaR, 组合的VaR
author: 姜春妮
'''
import numpy as np
from statsmodels.formula.api import quantreg
from sympy import symbols, Eq, solve

from volRet import vol_return,stk_vol_ret


#%%
# 计算VaR
# quantiles = [.01, .05, .25, .5, .75, .95]
# C = .95  # 置信水平


def get_VaR(result, quantiles, C): # 计算组合VaR
    mod = quantreg('portfolio_return ~ portfolio_vol_std + p_vol_std_square',result) # y~x1+x2, data
    VaR_list = []
    for q in quantiles:
        res = mod.fit(q)
        pred_y = sorted(res.predict(result[['portfolio_vol_std','p_vol_std_square']])) # 从小到大
        VaR_list.append(np.percentile(pred_y,C))

    VaR = np.average(VaR_list)
    return VaR


def get_stk_VaR(result, quantiles, C): # 计算各资产VaR
    mod = quantreg('ret ~ vol + vol_square', result)  # y~x1+x2, data
    VaR_list = []
    for q in quantiles:
        res = mod.fit(q)
        pred_y = sorted(res.predict(result[['vol', 'vol_square']]))  # 从小到大
        VaR_list.append(np.percentile(pred_y, C))

    VaR = np.average(VaR_list)
    return -VaR

# res2 = get_stk_VaR(res,quantiles,C)

def get_p_VaR(VaRs,w,rou): # 基于各资产VaR计算组合VaR
    value1  = np.sum([(w[i]**2)*(VaRs[i]**2) for i in range(len(VaRs))])
    value2 = 2*w[0]*w[1]*rou[0]*VaRs[0]*VaRs[1] + 2*w[0]*w[2]*rou[1]*VaRs[0]*VaRs[2] + 2*w[1]*w[2]*rou[2]*VaRs[1]*VaRs[2]
    return value1+value2

# stk_name = 'bank'
# distribution = 'std'
# bank = stk_vol_ret(data,vol,'bank',distribution)
# defense = stk_vol_ret(data,vol,'defense',distribution)
# food = stk_vol_ret(data,vol,'food',distribution)
#
# VaR1 = get_stk_VaR(bank,quantiles,C)
# VaR2 = get_stk_VaR(defense,quantiles,C)
# VaR3 = get_stk_VaR(food,quantiles,C)
#
# w1=.3
# w2=.5
# w3=.2
# w=[w1,w2,w3]
#
# rou = [0.334827,0.434386,0.540143]
#
# VaR_p = get_p_VaR([VaR1,VaR2,VaR3],w,rou)


#%%
# 计算VaR对wi的偏导
def get_diff_VaR(data_cal, vol_cal, w, delta_w, quantiles, C): # w=[w1,w2,w3]

    result_minus_1 = vol_return(data_cal,vol_cal,w[0]-delta_w,w[1],w[2])
    result_plus_1 = vol_return(data_cal,vol_cal,w[0]+delta_w,w[1],w[2])
    diff_VaR_1 = (get_VaR(result_plus_1,quantiles, C)-get_VaR(result_minus_1,quantiles, C))/(2*delta_w)

    result_minus_2 = vol_return(data_cal, vol_cal, w[0], w[1] - delta_w, w[2])
    result_plus_2 = vol_return(data_cal, vol_cal, w[0] , w[1] + delta_w, w[2])
    diff_VaR_2 = (get_VaR(result_plus_2,quantiles, C) - get_VaR(result_minus_2,quantiles, C)) / (2 * delta_w)

    result_minus_3 = vol_return(data_cal, vol_cal, w[0], w[1], w[2] - delta_w)
    result_plus_3 = vol_return(data_cal, vol_cal, w[0], w[1], w[2] + delta_w)
    diff_VaR_3 = (get_VaR(result_plus_3,quantiles, C) - get_VaR(result_minus_3,quantiles, C)) / (2 * delta_w)

    return diff_VaR_1,diff_VaR_2,diff_VaR_3


# diff_VaR_1,diff_VaR_2,diff_VaR_3 = get_diff_VaR(data,vol,w,.01,quantiles,C)

def get_diff_VaR_stk(data, vol, stk_names,distribution, quantiles, C, w, rou): # 基于各资产VaR计算组合VaR的偏导
    data1 = stk_vol_ret(data, vol, stk_names[0], distribution)
    data2 = stk_vol_ret(data, vol, stk_names[1], distribution)
    data3 = stk_vol_ret(data, vol, stk_names[2], distribution)

    VaR1 = get_stk_VaR(data1, quantiles, C)
    VaR2 = get_stk_VaR(data2, quantiles, C)
    VaR3 = get_stk_VaR(data3, quantiles, C)
    VaRs = [VaR1, VaR2, VaR3]

    diff1 = 2*w[0]*VaRs[0] + 2*w[1]*rou[0]*VaRs[0]*VaRs[1] + 2*w[2]*rou[1]*VaRs[0]*VaRs[2]
    diff2 = 2*w[1]*VaRs[1] + 2*w[2]*rou[0]*VaRs[0]*VaRs[1] + 2*w[2]*rou[2]*VaRs[1]*VaRs[2]
    diff3 = 2*w[2]*VaRs[2] + 2*w[0]*rou[1]*VaRs[0]*VaRs[2] + 2*w[1]*rou[2]*VaRs[1]*VaRs[2]

    return diff1, diff2, diff3


# diff1, diff2, diff3 = get_diff_VaR_stk(data, vol, ['bank','defense','food'],'std',quantiles,C,w,rou)


# bank = stk_vol_ret(data, vol, 'bank', distribution)
# VaR1 = get_stk_VaR(bank,quantiles,C)
# VaRs = [VaR1, VaR2, VaR3]
# diff1 = get_diff_VaR_1(VaRs, w, rou, 1)
# diff2 = get_diff_VaR_1(VaRs, w, rou, 2)
# diff3 = get_diff_VaR_1(VaRs, w, rou, 3)

#%%
# 计算w
def solve_w(diff_VaR_1,diff_VaR_2,diff_VaR_3):
    w1,w2,w3 = symbols('w1,w2,w3')

    eq1 = Eq((w1+w2+w3), 1)
    eq2 = Eq((diff_VaR_1*w1-diff_VaR_2*w2), 0)
    eq3 = Eq((diff_VaR_1*w1-diff_VaR_3*w3), 0)

    ans = solve((eq1, eq2, eq3), (w1,w2,w3))
    return ans[w1],ans[w2],ans[w3]


# w1,w2,w3 = solve_w(diff_VaR_1,diff_VaR_2,diff_VaR_3)