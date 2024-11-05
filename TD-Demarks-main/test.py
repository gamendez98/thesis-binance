from classes.TDComboTrader import TDComboTrader
import pandas as pd

df = pd.read_csv('test_data.csv')  
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

trader = TDComboTrader(df2, parameters)

for index, row in df.iterrows():
    row_dict = row.to_dict()
    trader.updateInformation(row_dict)
    