# 基于分位数回归计算VaR值的风险平价模型

金融计量学期末课程论文核心代码
auther：姜春妮 张宇萌 刘袁吟泉 屠心怡

## 目录结构

### data

    指数数据2.xlsx   原始数据，从中选择bank defense food
    index.csv       指数数据
    data.csv        资产的日对数收益率
    vol.csv         GARCH模型在不同分布下估计得到的日波动率

### result

    distribution.csv    不同分布假设下的组合价值
    freq.csv            不同调仓频率下的组合价值
    back.csv            计算VaR的回望时长取不同值得到的组合价值
    quantiles.csv       分位数取不同值得到的组合价值
    weight.csv          和等权重、固定权重模型的比较


## 代码结构

process.py      检验资产收益率的相关性，及ADF检验、自相关性和偏自相关性检验
get_vol.R       在不同分布假设下使用GARCH模型估计单资产波动率
volRet.py       计算组合的收益率和波动率
frequency.py    将数据按照单月分割，便于后续使用
VaR.py          计算各资产的VaR值及组合VaR值，计算每次调仓的权重
accRet.py       主函数，得出该策略下组合价值的变化
analysis.py     效果评价

## 调参说明

freq                调仓频率
back                计算VaR的回望时长/调仓频率的倍数
w                   初始权重
money               初始资产分配，与初始权重对应
quantiles           分位数
get_diff_VaR_stk    在函数的参数中选择分布


## 运行代码

run accRet.py 
当前参数设置下所得结果存储在 result.csv 中