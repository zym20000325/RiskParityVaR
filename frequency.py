'''
根据给定的调仓频率来把data分割成一个个小的dataframe
author: 张宇萌
'''
import pandas as pd

def month(s):
    loc1 = s.find('/')
    loc2 = s[loc1 + 1:].find('/') + loc1 + 1

    month = s[loc1 + 1:loc2]

    return month


# 分割成单月

def one_month_cut(data):
    data_month = []

    start = 0
    end = 1

    while (end <= len(data) - 1):

        if (month(data['datetime'][start]) == month(data['datetime'][end])):

            end = end + 1

        else:

            #             print(month(data['datetime'][start]))
            #             print(month(data['datetime'][end]))

            one_month = data[start:end]
            data_month.append(one_month)
            start = end

    one_month = data[start:]
    data_month.append(one_month)

    #     print(len(data_month))

    return data_month


# 按频率分割

def frequency_cut(data_return, data_vol, data_index, freq):
    returnset = []  # 存储分割后的组合收益率
    volset = []  # 存储分割后的组合波动率
    indexset = []  # 存储分割后的指数

    # 首先按照单月分割

    data_return_month = one_month_cut(data_return)
    data_vol_month = one_month_cut(data_vol)
    data_index_month = one_month_cut(data_index)



    # 固定频率

    if (type(freq) == int):

        if (freq == 1):

            return data_return_month, data_vol_month, data_index_month

        else:

            start = 0
            end = freq

            while (end <= len(data_return_month) - 1):
                # print(data_return_month[start:end])
                one_period = pd.concat(data_return_month[start:end])
                returnset.append(one_period)

                one_vol_period = pd.concat(data_vol_month[start:end])
                volset.append(one_vol_period)

                one_index_period = pd.concat(data_index_month[start:end])
                indexset.append(one_index_period)

                start = start + freq
                end = end + freq

            # zym 8.5 改 最后一小段不要了
            # returnset.append(data_return_month[start:]) 
            # volset.append(data_vol_month[start:])
            # indexset.append(data_index_month[start:])

            return returnset, volset, indexset


# 例子

# data = pd.read_csv("data.csv")  # 组合收益率
# data_vol = pd.read_csv("vol.csv")  # 组合波动率
# data_index = pd.read_csv("index.csv")  # 指数
#
# freq = 3
#
# returnset, volset, indexset = frequency_cut(data, data_vol, data_index, freq)
#
# print(returnset[1])
# print(volset[1])
# print(indexset[1])
#
# print(len(returnset))
# print(len(volset))
# print(len(indexset))