import numbers
from enum import Enum

from td_demarks_main.classes.TDBuySetup import TDBuySetup
from td_demarks_main.classes.TDSellSetup import TDSellSetup


class Signal(int, Enum):
    BUY = 1
    SELL = -1
    NONE = 0


class TDComboTrader:
    def __init__(self, df, parameters):

        self.df = df  # Price information
        self.parameters = parameters

        self.completed_buy_setups = []
        self.completed_sell_setups = []

        self.active_buy_setup = None  # The attribute that checks wether a new setup exists
        self.active_sell_setup = None

        self.completed_buy_setup = False
        self.completed_sell_setup = False

        self.completed_buy_countdowns = []
        self.canceled_buy_countdowns = []

        self.completed_sell_countdowns = []
        self.canceled_sell_countdowns = []

        self.active_buy_countdown = False  # The attribute that checks wether a countdown exists
        self.active_sell_countdown = False

        self.tdst_support = None
        self.tdst_resistance = None

        self.long = False
        self.longEntry = None
        self.short = False
        self.shortEntry = None

    def trade(self, information_stream):
        signals = []
        for information in information_stream:
            self.updateInformation(information)
            l, s = self.longTrade(), self.shortTrade()
            signals.append(l + s)
        return signals

    def checkBuyCountdownCancelation(self, information):
        if self.active_buy_countdown != None:
            if (information["low"] > self.tdst_resistance) or (
                    self.completed_sell_setups[-1].sell_setup_index >= self.active_buy_countdown.countdown_indices[0]):
                self.active_buy_countdown.cancelCountdown()
                self.canceled_buy_countdowns.append(self.active_buy_countdown)
                self.active_buy_countdown = None

    def checkSellCountdownCancelation(self, information):
        if self.active_sell_countdown != None:
            if (information["high"] < self.tdst_support) or (
                    self.completed_buy_setups[-1].buy_setup_index >= self.active_sell_countdown.countdown_indices[0]):
                self.active_sell_countdown.cancelCountdown()
                self.canceled_sell_countdowns.append(self.active_sell_countdown)
                self.active_buy_countdown = None

    def updateInformation(self, information):
        if not self.validInformation(information):
            return

        self.completed_buy_setup = False
        self.completed_sell_setup = False

        self.df.loc[len(self.df)] = information
        index = len(self.df) - 1
        # If there is an active setup, update.
        if self.active_buy_setup is not None:
            if self.active_buy_setup.updateInformation():
                self.completed_buy_setups.append(self.active_buy_setup)
                self.tdst_resistance = self.active_buy_setup.maximum
                self.tdst_support = self.active_buy_setup.minimum
                self.active_buy_setup = None
                self.completed_buy_setup = True
        # If not, check wether it can be created
        else:
            self.active_buy_setup = TDBuySetup(self, index, self.parameters)

        if self.active_sell_setup is not None:
            if self.active_sell_setup.updateInformation():
                self.completed_sell_setups.append(self.active_sell_setup)
                self.tdst_resistance = self.active_sell_setup.maximum
                self.tdst_support = self.active_sell_setup.minimum
                self.active_sell_setup = None
                self.completed_sell_setup = True
        else:
            self.active_sell_setup = TDSellSetup(self, index, self.parameters)

        self.checkBuyCountdownCancelation(information)
        self.checkSellCountdownCancelation(information)

    def validInformation(self, information):
        required_keys = {
            'time': numbers.Number,
            'open': numbers.Number,
            'high': numbers.Number,
            'low': numbers.Number,
            'close': numbers.Number}

        for key, value_type in required_keys.items():
            if key not in information:
                return False
            if not isinstance(information[key], value_type):
                return False
        return True

    def buyBackend(self, information):
        None  # Connect to binance or other exchange

    def sellBackend(self, information):
        None  # Connect to binance or other exchange

    def longTrade(self):
        if self.completed_buy_setup:
            if not self.long:
                self.buyBackend(self.df.iloc[-1])
                self.long = True
                return Signal.BUY
            else:
                if self.df.iloc[-1]["close"] <= self.longEntry * 0.98:
                    self.sellBackend(self.df.iloc[-1])
                    self.long = False
                    return Signal.SELL
                elif self.df.iloc[-1]["close"] >= self.longEntry * 1.02:
                    self.sellBackend(self.df.iloc[-1])
                    self.long = False
                    return Signal.SELL
        return Signal.NONE

    def shortTrade(self):
        if self.completed_sell_setup:
            if not self.short:
                self.sellBackend(self.df.iloc[-1])
                self.short = True
                return Signal.SELL
            else:
                if self.df.iloc[-1]["close"] >= self.shortEntry * 1.02:
                    self.buyBackend(self.df.iloc[-1])
                    self.short = False
                    return Signal.BUY
                elif self.df.iloc[-1]["close"] <= self.shortEntry * 0.98:
                    self.buyBackend(self.df.iloc[-1])
                    self.short = False
                    return Signal.BUY
        return Signal.NONE
