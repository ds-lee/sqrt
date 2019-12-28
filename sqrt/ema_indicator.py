import pandas as pd
from sqrt.ta_indicator import TAIndicator
from sqrt.utils import *

class EMAIndicator(TAIndicator):

    def __init__(self, ct:pd.DataFrame, pairs: dict, lead: int, lag: int, prices, price_returns, price_norms):
        self.ct = ct
        self.pairs = pairs
        self.lead = lead
        self.lag = lag
        self.prices = prices
        self.price_returns = price_returns
        self.price_norms = price_norms

    def ema(self, df, span):
        return df.ewm(span=span, min_periods=0, adjust=False, ignore_na=False).mean()

    def signal(self) -> pd.DataFrame:
        ema_signal = pd.DataFrame(0, index=self.price_returns.index, columns=self.pairs)
        for pair in self.pairs:
            ema_signal[pair] = self.ema(self.prices[pair], self.lead) > self.ema(self.prices[pair], self.lag)
        return ema_signal
