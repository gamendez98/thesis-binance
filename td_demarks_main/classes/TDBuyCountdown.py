class TDBuyCountdown:
    def __init__(self, tdTrader, tdBuySetup, parameters, index):
        self.index = index
        self.tdTrader = tdTrader
        self.tdBuySetup = tdBuySetup
        self.countdown = 0
        self.countdown_indices = []
        self.param_countdown = parameters["TDComboBuyCountdown"]["param_countdown"]
        self.param_previous_bars = parameters["TDComboBuyCountdown"]["param_previous_bars"]
        self.param_bar_to_compare = parameters["TDBuyCountdown"]["param_bar_to_compare"]
        self.completed = False
        self.canceled = False

        self.initializeCountdown()
        
    def initializeCountdown(self):
        for i in range(0,self.tdBuySetup.param_consecutive):
            self.updateInformation(self,self.tdBuySetup.index + 1 + i)
    
    def updateInformation(self,index):
        previous_close = self.tdTrader.df.loc[self.index-1,"close"]
        previous_low = self.tdTrader.df.loc[self.index-1,"low"]
        previous_tdCountdown_close = self.tdTrader.df.loc[self.countdown_indices[-1],"close"]

        flag = True
        if self.tdTrader.df["close"].iloc[index] > self.tdTrader.df["close"].iloc[index-self.param_previous_bars]:
                flag = False

        new_flag = True 
        if self.tdTrader.df["close"].iloc[index] > previous_low:
            new_flag = True
        elif self.tdTrader.df["close"].iloc[index] >= previous_tdCountdown_close:
            new_flag = True
        elif self.tdTrader.df["close"].iloc[index] >= previous_close:
            new_flag = True

        if flag and new_flag:
            self.countdown += 1
            self.countdown_indices.append(self.tdBuySetup.buy_setup_index)

        if self.countdown >= self.param_countdown:
            self.checkCompletion(index)
        self.tdTrader.checkBuyCountdownCancelation()
    
    def checkCompletion(self,index):
        if self.tdTrader.df["low"].iloc[index] <= self.tdTrader.df["close"].iloc[self.countdown_indices[self.param_bar_to_compare]]:
            flag = True
            for i in range(self.param_previous_bars):
                if self.tdTrader.df["close"].iloc[index] > self.tdTrader.df["close"].iloc[index-(i+1)]:
                    flag = False
            if flag:
                self.completed = True

    def cancelCountdown(self):
        self.canceled = True