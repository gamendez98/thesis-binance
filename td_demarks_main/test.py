from td_demarks_main.classes.TDComboTrader import TDComboTrader
import pandas as pd


def main():
    df = pd.read_csv('td_demarks_main/test_data.csv')
    df2 = pd.DataFrame(columns=df.columns)

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
            "param_bar_to_compare":1
        }

    }

    def information_stream(data):
        for _, row in data.iterrows():
            yield row.to_dict()

    trader = TDComboTrader(df2, parameters)

    signals = trader.trade(information_stream(df))
    print(signals)

if __name__ == "__main__":
    main()
    