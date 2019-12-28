import pandas as pd


Fee = 0.002
MAR = 0

def get_return(v_f, v_i):
    return (v_f - v_i)/v_i


def lpm(ret):  # mean(min(MAR, ret).^2)
    _lpm = ret.copy()
    _lpm.loc[_lpm > MAR] = 0
    return _lpm.mul(_lpm).mean()


def normalize(arr):
    return (arr - arr.min()) / (arr.max() - arr.min())


def tick2ret(price_tick):
    return price_tick/price_tick.shift(1) - 1


def compute_price_returns(candle_tables, opts):
    prices = pd.DataFrame(0, index=candle_tables[2].index, columns=opts)
    for i, opt in enumerate(opts):
        prices[opt] = candle_tables[i]['Close']
    priceReturns = tick2ret(prices)
    priceNorm = normalize(prices)
    return prices, priceReturns, priceNorm


def compute_return_from_signal(price_returns, signals, opts):
    fee = Fee * signals.diff(1, 0).abs().sum(1)
    ret = price_returns[1:-1].mul(signals[1:-1]).sum(1) - fee
    cumret = (1 + ret).cumprod()
    cumret_max = cumret.cummax()
    mdd = ((cumret - cumret_max)/cumret_max).min()
    daily_ret = ret.groupby(ret.index.date).sum()
    sharpe_ratio = ret.mean() / ret.std()
    sortino_ratio = ret.mean() / (lpm(ret)**0.5)
    sharpe = (525949)**0.5 * sharpe_ratio
    sortino = (525949)**0.5 * sortino_ratio
    return ret, cumret, mdd, sharpe, sortino


def evaluate(_price_return, signal, opts, delay=0):
    signals_base_mat = pd.DataFrame(0, index=_price_return.index, columns=opts)
    for opt in opts:
        signals_base_mat[opt] = signal[opt]
    signals_base_mat = signals_base_mat.astype(float)
    signals_base_mat = signals_base_mat.div(len(opts))
    signals_base_mat = signals_base_mat.shift(delay)
    assert signals_base_mat.sum(1).max() < 1.0001, f"sum(signal_base_mat)(={signals_base_mat.sum(1).max()}) cannot be larger than 1.0"
    signals_base_mat.sum(1)
    ret, cumret, mdd, sharpe, sortino = compute_return_from_signal(_price_return.loc[_price_return.index < '2019-11-02'],
                                                                   signals_base_mat.loc[_price_return.index < '2019-11-02'],
                                                                   opts)
    return mdd, sharpe, sortino, cumret
