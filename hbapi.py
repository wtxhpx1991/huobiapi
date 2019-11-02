#根据火币网提供的接口开发行情获取、账户信息获取及下单程序

from utils import *

ACCOUNT_ID = 755426


# 获取KLine
def get_kline(symbol, period, size=150):
    """
    :param symbol
    :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param size: 可选值： [1,2000]
    :return:
    """
    params = {'symbol': symbol,
              'period': period,
              'size': size}

    url = MARKET_URL + '/market/history/kline'
    return http_get_request(url, params)


# 获取marketdepth
def get_depth(symbol, type):
    """
    :param symbol
    :param type: 可选值：{ percent10, step0, step1, step2, step3, step4, step5 }
    :return:
    """
    params = {'symbol': symbol,
              'type': type}

    url = MARKET_URL + '/market/depth'
    return http_get_request(url, params)


# 获取tradedetail
def get_trade(symbol):
    """
    :param symbol
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/trade'
    return http_get_request(url, params)


# Tickers detail
def get_tickers():
    """
    :return:
    """
    params = {}
    url = MARKET_URL + '/market/tickers'
    return http_get_request(url, params)


# 获取merge ticker
def get_ticker(symbol):
    """
    :param symbol:
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/detail/merged'
    return http_get_request(url, params)


# 获取 Market Detail 24小时成交量数据
def get_detail(symbol):
    """
    :param symbol
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/detail'
    return http_get_request(url, params)


# 获取  支持的交易对
def get_symbols(long_polling=None):
    """
    """
    params = {}
    if long_polling:
        params['long-polling'] = long_polling
    path = '/v1/common/symbols'
    return api_key_get(params, path)


# Get available currencies
def get_currencies():
    """
    :return:
    """
    params = {}
    url = MARKET_URL + '/v1/common/currencys'

    return http_get_request(url, params)


# Get all the trading assets
def get_trading_assets():
    """
    :return:
    """
    params = {}
    url = MARKET_URL + '/v1/common/symbols'

    return http_get_request(url, params)


def get_accounts():
    """
    获取账户信息
    :return:
    """
    path = "/v1/account/accounts"
    params = {}
    return api_key_get(params, path)


ACCOUNT_ID = 0


# 获取当前账户资产
def get_balance(acct_id=None):
    """
    :param acct_id
    :return:
    """
    global ACCOUNT_ID

    if not acct_id:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id'];

    url = "/v1/account/accounts/{0}/balance".format(acct_id)
    params = {"account-id": acct_id}
    return api_key_get(params, url)


def send_order(amount, source, symbol, _type, price=0):
    """
    创建并执行订单
    :param amount:
    :param source: 如果使用借贷资产交易，请在下单接口,请求参数source中填写'margin-api'
    :param symbol:
    :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param price:
    :return:
    """
    try:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id']
    except BaseException as e:
        print('get acct_id error.%s' % e)
        acct_id = ACCOUNT_ID

    params = {"account-id": acct_id,
              "amount": amount,
              "symbol": symbol,
              "type": _type,
              "source": source}
    if price:
        params["price"] = price

    url = '/v1/order/orders/place'
    return api_key_post(params, url)


def cancel_order(order_id):
    """
    撤销订单
    :param order_id:
    :return:
    """
    params = {}
    url = "/v1/order/orders/{0}/submitcancel".format(order_id)
    return api_key_post(params, url)


def order_info(order_id):
    """
    查询某个订单
    :param order_id:
    :return:
    """
    params = {}
    url = "/v1/order/orders/{0}".format(order_id)
    return api_key_get(params, url)


def order_matchresults(order_id):
    """
    查询某个订单的成交明细
    :param order_id:
    :return:
    """
    params = {}
    url = "/v1/order/orders/{0}/matchresults".format(order_id)
    return api_key_get(params, url)


def orders_list(symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    查询当前委托、历史委托
    :param symbol:
    :param states: 可选值 {pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销}
    :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param start_date:
    :param end_date:
    :param _from:
    :param direct: 可选值{prev 向前，next 向后}
    :param size:
    :return:
    """
    params = {'symbol': symbol,
              'states': states}

    if types:
        params['types'] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    url = '/v1/order/orders'
    return api_key_get(params, url)


def orders_matchresults(symbol, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    查询当前成交、历史成交
    :param symbol:
    :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param start_date:
    :param end_date:
    :param _from:
    :param direct: 可选值{prev 向前，next 向后}
    :param size:
    :return:
    """
    params = {'symbol': symbol}

    if types:
        params['types'] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    url = '/v1/order/matchresults'
    return api_key_get(params, url)


def open_orders(account_id, symbol, side='', size=10):
    """
    查询所有当前帐号下未成交订单
    :param symbol:
    :return:
    """
    params = {}
    url = "/v1/order/openOrders"
    if symbol:
        params['symbol'] = symbol
    if account_id:
        params['account-id'] = account_id
    if side:
        params['side'] = side
    if size:
        params['size'] = size

    return api_key_get(params, url)


def cancel_open_orders(account_id, symbol, side='', size=10):
    """
    批量取消符合条件的订单
    :param symbol:
    :return:
    """
    params = {}
    url = "/v1/order/orders/batchCancelOpenOrders"
    if symbol:
        params['symbol'] = symbol
    if account_id:
        params['account-id'] = account_id
    if side:
        params['side'] = side
    if size:
        params['size'] = size

    return api_key_post(params, url)
