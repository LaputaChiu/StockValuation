import pysnooper
import pandas as pd
#import yfinance as yf
import yahoo_fin.stock_info as si
import math

def to_calc_value(val: str) -> float:
    return round(float(val), 2)

class Stats:
    def __init__(self, ticker: str):
        self.stats = si.get_stats(ticker)
        self.stats = self.stats.set_index('Attribute')

    def get_NAV(self) -> float:
        return to_calc_value(self.stats.loc['Book Value Per Share (mrq)']['Value'])
    
    def get_ROE(self) -> float:
        roe = str(self.stats.loc['Return on Equity (ttm)']['Value'])
        if roe[-1] != '%':
            return float('nan')
        return to_calc_value(roe[:-1]) / 100

class StatsValuation:
    def __init__(self, ticker: str):
        self.stats = si.get_stats_valuation(ticker)
        self.stats = self.stats.set_index(0)

    def get_PS(self) -> float:
        return to_calc_value(self.stats.loc['Price/Sales (ttm)'][1])


class QuoteTable:
    def __init__(self, ticker: str):
        self.stats = si.get_quote_table(ticker, dict_result=False)
        self.stats = self.stats.set_index('attribute')

    def get_PE(self) -> float:
        return to_calc_value(self.stats.loc['PE Ratio (TTM)']['value'])

    def get_EPS(self) -> float:
        return to_calc_value(self.stats.loc['EPS (TTM)']['value'])

class Profile:
    def __init__(self, ticker: str):
        self.prof = si.get_company_info(ticker)

    def get_Indus(self) -> str:
        return self.prof.loc['industry']['Value']

def get_current_price(ticker: str) -> float:
    return to_calc_value(si.get_live_price(ticker))

###########################################################################################################
# class DataSheetGenerator():
#     def __init__(self, ticker: str):
#         self._val = float('nan')
#         self._book_val_mrq = float('nan')
#         self._roe_ttm = float('nan')
#         self._per_ttm = float('nan')
#         self._est_eps = float('nan')
#         self._est_val = float('nan')
    
#     @staticmethod
#     def check_float(data) -> float:
#         if type(data) == float:
#             return data
#         else:
#             raise TypeError('data need float.')

#     @property
#     def val(self):
#         return self._val

#     @val.setter
#     def val(self, data):
#         self._val = DataSheetGenerator.check_float(data)

#     @property
#     def book_val_mrq(self):
#         return self._book_val_mrq

#     @book_val_mrq.setter
#     def book_val_mrq(self, data):
#         self._book_val_mrq = DataSheetGenerator.check_float(data)

#     @property
#     def roe_ttm(self):
#         return self._roe_ttm

#     @roe_ttm.setter
#     def roe_ttm(self, data):
#         self._roe_ttm = DataSheetGenerator.check_float(data)

#     @property
#     def per_ttm(self):
#         return self.per_ttm

#     @per_ttm.setter
#     def per_ttm(self, data):
#         self._per_ttm = DataSheetGenerator.check_float(data)

#     @property
#     def est_eps(self):
#         return self.est_eps

#     @est_eps.setter
#     def est_eps(self, data):
#         self._est_eps = DataSheetGenerator.check_float(data)

#     @property
#     def est_val(self):
#         return self.est_val

#     @est_val.setter
#     def est_val(self, data):
#         self._est_val = DataSheetGenerator.check_float(data)
###########################################################################################################
labels = ['Industry', 'Current val', 'Book val (mrq)', 'ROE % (ttm)', 'P/E Ratio (ttm)', 'P/S Ratio (ttm)', 'Est. Eps', 'Est. Val', 'Est Earn %', 'Est. Val -10%', 'Est. Val +10%']

#@pysnooper.snoop()
def evaluate_data(ticker: str) -> list:
    stats = Stats(ticker)
    stats_valuation = StatsValuation(ticker)
    quote = QuoteTable(ticker)
    profile = Profile(ticker)

    roe = stats.get_ROE()
    nav = stats.get_NAV()
    est_eps = roe * nav

    pe = quote.get_PE()
    est_val = est_eps * pe

    return [profile.get_Indus(), get_current_price(ticker), nav, roe, quote.get_PE(), stats_valuation.get_PS(), est_eps, est_val, (est_val - get_current_price(ticker)) / get_current_price(ticker) * 100, est_val - (est_val / 10), est_val + (est_val / 10)]


def evaluate(ticker_list: list) -> pd.DataFrame:
    data = []

    for ticker in ticker_list:
        data.append(evaluate_data(ticker))

    df = pd.DataFrame(data, ticker_list, labels)
    #df = df.sort_values(by=[labels[0]])
    return df
    

if __name__ == '__main__':

    tw_ticker_list = ['3033.tw', '1464.tw', '2002.tw', '2881.tw', '2883.tw', '2882.tw','2353.tw', '2451.tw', '2006.tw']
    tw_data = evaluate(tw_ticker_list)
    print(tw_data)

    #'PLTR', 'PATH', 'APPS', 'TDOC', 'AMZN', 'AAPL', 'ADBE', 'ASAN', 'CRWD', 'S', 'FB', 'MDB', 'MSFT', 'NET', 'NFLX', 'SPOT', 'TSLA', 'U', 'UPST', 'ZIM', 'GRMN', 'ZM','ECOM','AMD','NVDA', 'AMPL','SSYS', 'SQ'
    us_ticker_list = ['UPST','PLTR', 'PATH', 'TDOC', 'S', 'AMD', 'NVDA']
    us_data = evaluate(us_ticker_list)
    print(us_data)