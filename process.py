'''
数据处理：相关性、ADF检验、自相关性、偏自相关性
author: 姜春妮
'''
import pandas as pd
import sys
from statsmodels.tsa.stattools import adfuller,acf,pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

#%%
path = 'data/data.csv'
sys.path.insert(0,'.')
data_full = pd.read_csv(path)

#%%
data = data_full[['bank','defense','food']]

#%%
# 相关性
cor = data.corr()

#%%
#ADF test
print(adfuller(data.loc[:,'defense']))

#%%
#自相关
auto_c = acf(data.loc[:,'defense']) #各阶自相关系数
plt=plot_acf(data.loc[:,'defense']) #根据各阶自相关系数画出的图
plt.show()
print(auto_c)


#偏自相关
pauto_c = pacf(data.loc[:,'defense'])
plt = plot_pacf(data.loc[:,'defense'])
plt.show()
print(pauto_c)
