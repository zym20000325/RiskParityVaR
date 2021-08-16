'''
计算组合波动率、收益率
author: 张宇萌、姜春妮
'''
import pandas as pd
import numpy as np
from datetime import datetime
import datetime



def portfolio_return(data, w1, w2, w3):
    data['portfolio_return'] = (w1 * data['bank'] + w2 * data['defense'] + w3 * data['food']).astype('float')
    return data


def portfolio_vol(vol, w1, w2, w3):
    # std

    sigma11 = vol['bank_std'].astype('float')
    sigma12 = vol['defense_std'].astype('float')
    sigma13 = vol['food_std'].astype('float')
    vol["portfolio_vol_std"] = (w1 * w1 * sigma11 * sigma11 + w2 * w2 * sigma12 * sigma12 + w3 * w3 * sigma13 * sigma13 \
                                + 2 * w1 * w2 * 0.334827 * sigma11 * sigma12 + 2 * w2 * w3 * 0.540143 * sigma12 * sigma13 \
                                + 2 * w1 * w3 * 0.434386 * sigma11 * sigma13) ** 0.5

    # sstd

    sigma21 = vol['bank_sstd'].astype('float')
    sigma22 = vol['defense_sstd'].astype('float')
    sigma23 = vol['food_sstd'].astype('float')
    vol["portfolio_vol_sstd"] = (w1 * w1 * sigma21 * sigma21 + w2 * w2 * sigma22 * sigma22 + w3 * w3 * sigma23 * sigma23 \
                                 + 2 * w1 * w2 * 0.334827 * sigma21 * sigma22 + 2 * w2 * w3 * 0.540143 * sigma22 * sigma23 \
                                 + 2 * w1 * w3 * 0.434386 * sigma21 * sigma23) ** 0.5

    # ged

    sigma31 = vol['bank_ged'].astype('float')
    sigma32 = vol['defense_ged'].astype('float')
    sigma33 = vol['food_ged'].astype('float')
    vol["portfolio_vol_ged"] = (w1 * w1 * sigma31 * sigma31 + w2 * w2 * sigma32 * sigma32 + w3 * w3 * sigma33 * sigma33 \
                                + 2 * w1 * w2 * 0.334827 * sigma31 * sigma32 + 2 * w2 * w3 * 0.540143 * sigma32 * sigma33 \
                                + 2 * w1 * w3 * 0.434386 * sigma31 * sigma33) ** 0.5

    # sged

    sigma41 = vol['bank_sged'].astype('float')
    sigma42 = vol['defense_sged'].astype('float')
    sigma43 = vol['food_sged'].astype('float')
    vol["portfolio_vol_sged"] = (w1 * w1 * sigma41 * sigma41 + w2 * w2 * sigma42 * sigma42 + w3 * w3 * sigma43 * sigma43 \
                                 + 2 * w1 * w2 * 0.334827 * sigma41 * sigma42 + 2 * w2 * w3 * 0.540143 * sigma42 * sigma43 \
                                 + 2 * w1 * w3 * 0.434386 * sigma41 * sigma43) ** 0.5

    return vol


def vol_return(data, data_vol, w1, w2, w3):
    data1 = portfolio_return(data, w1, w2, w3)
    data2 = portfolio_vol(data_vol, w1, w2, w3)

    result = data1
    result['portfolio_vol_std'] = data2['portfolio_vol_std'].astype('float')
    result['portfolio_vol_sstd'] = data2['portfolio_vol_sstd'].astype('float')
    result['portfolio_vol_ged'] = data2['portfolio_vol_ged'].astype('float')
    result['portfolio_vol_sged'] = data2['portfolio_vol_sged'].astype('float')

    result['p_vol_std_square'] = (result['portfolio_vol_std'] * result['portfolio_vol_std']).astype('float')
    result['p_vol_sstd_square'] = (result['portfolio_vol_sstd'] * result['portfolio_vol_sstd']).astype('float')
    result['p_vol_ged_square'] = (result['portfolio_vol_ged'] * result['portfolio_vol_ged']).astype('float')
    result['p_vol_sged_square'] = (result['portfolio_vol_sged'] * result['portfolio_vol_sged']).astype('float')

    result = result.drop(labels=['bank', 'defense', 'food'], axis=1)


    # filename = "w1=" + str(w1) + "_w2=" + str(w2) + "_w3=" + str(w3) + ".csv"
    # result.to_csv(filename)

    return result

#%%
# import sys
# import pandas as pd
#
# path_data = 'data/data.csv'
# path_vol = 'data/vol.csv'
# path_idx = 'data/index.csv'
#
# sys.path.insert(0,'.')
# data = pd.read_csv(path_data)
# vol = pd.read_csv(path_vol)
# index = pd.read_csv(path_idx)


#%%

def stk_vol_ret(data, vol, stk_name, distribution):
    stk_data = pd.DataFrame()
    stk_data['datetime'] = data['datetime']
    stk_data['ret'] = data[stk_name].astype('float')
    stk_data['vol'] = vol[stk_name + '_' + distribution].astype('float')
    stk_data['vol_square'] = (vol[stk_name + '_' + distribution] ** 2).astype('float')
    return stk_data

# stk_name = 'bank'
# distribution = 'std'
# bank = stk_vol_ret(data,vol,'bank',distribution)
# defense = stk_vol_ret(data,vol,'defense',distribution)
# food = stk_vol_ret(data,vol,'food',distribution)
