import numpy as np
import pandas as pd

from td_demarks_main.classes.TDComboTrader import TDComboTrader


# %%
def information_stream(data):
    for _, row in data.iterrows():
        info = row.to_dict()
        info['time'] = int(info['time'])
        yield info


# %%

def anatoley(signals, stock):
    last_value = stock.iloc[-1]
    stock_return = last_value - stock
    A = (stock_return * signals).mean()
    B = stock_return.mean() * signals.mean()
    p_ = (1 + signals.mean()) / 2
    V = (4 / len(signals)) * p_ * (1 - p_) * stock_return.std() ** 2
    return (A - B) / np.sqrt(V)


def main():
    snp_data = pd.read_csv('data/PYTH_SPY, 1D_91117.csv')
    df2 = pd.DataFrame(columns=snp_data.columns)

    parameters = {
        "TDComboBuySetup": {
            "param_consecutive": 4,
            "param_earlier": 2
        },
        "BearishTDPriceFlip": {
            "param_1": 2
        },
        "TDComboBuyCountdown": {
            "param_countdown": 1,
            "param_previous_bars": 1,
            "param_bar_to_compare": 1
        }

    }

    trader = TDComboTrader(df2, parameters)

    signals = trader.trade(information_stream(snp_data))
    print(anatoley(np.array(signals), snp_data['close']))


if __name__ == "__main__":
    main()