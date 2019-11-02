#本文档用于管理账户订单、资金、持仓情况
from hbapi import *
import pandas as pd

my_account=get_accounts()



def get_my_account_balance():
    '''
    获取账户里不为零的各类资产
    :return:
    '''
    my_account_balance = get_balance()
    list_num=len(my_account_balance['data']['list'])
    my_account_balance_dataframe=pd.DataFrame()
    for i in range(list_num):
        my_account_balance_dataframe=my_account_balance_dataframe.append(pd.DataFrame.from_dict(my_account_balance['data']['list'][i], orient='index').T)
    # my_account_balance_dataframe指账户的资产情况dataframe格式数据
    my_account_balance_dataframe[["balance"]] = my_account_balance_dataframe[["balance"]].astype(float)
    my_account_balance_dataframe_notzero=my_account_balance_dataframe[my_account_balance_dataframe['balance']>0]
    return my_account_balance_dataframe_notzero


my_account_balance_dataframe=get_my_account_balance() #当前账户还有多少资产

