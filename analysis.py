'''
指标计算
author: 屠心怡
'''

# 导入numpy包
import numpy as np

def MaxDrawdown(return_list):
    '''最大回撤率'''
    i = np.argmax((np.maximum.accumulate(return_list[0]) - return_list[0]) / np.maximum.accumulate(return_list[0]))  # 结束位置
    if i == 0:
        return 0
    j = np.argmax(return_list[0][:i])  # 开始位置
    return (return_list[0][j] - return_list[0][i]) / (return_list[0][j])

def sharpe_ratio(return_list):
    '''夏普比率'''
    average_return = np.mean(return_list[0])
    return_stdev = np.std(return_list[0])
    sharpe_ratio = (average_return-0.02/252) * np.sqrt(252) / return_stdev  #默认252个工作日,无风险利率为0.02
    return sharpe_ratio

# 计算股票的日平均收益
mean_return_daily = np.mean(clean_returns)
print("日平均收益：", mean_return_daily)
# 计算平均年化收益
mean_return_annualized = ((1 + mean_return_daily)**252) - 1
print("平均年化收益：", mean_return_annualized)