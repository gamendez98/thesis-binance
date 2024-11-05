class TDSellCountdown:
    def __init__(self, tdTrader, tdSellSetup, parameters,index):
        self.index = index
        self.tdTrader = tdTrader
        self.tdSellSetup = tdSellSetup
        self.countdown = 0
        self.countdown_indices = []
        self.param_countdown = parameters["TDComboSellCountdownV1"]["param_countdown"]
        self.param_bar_to_compare = parameters["TDComboSellCountdownV1"]["param_bar_to_compare"]
        self.param_previous_bars = parameters["TDComboSellCountdownV1"]["param_previous_bars"]
        self.completed = False
        self.canceled = False

        self.initializeCountdown()
        
    def initializeCountdown(self):
        for i in range(0,self.tdSellSetup.param_consecutive):
            self.updateInformation(self,self.tdSellSetup.index + 1 + i)

    def updateInformation(self,index):
        flag = True
        if self.tdTrader.df["close"].iloc[index] < self.tdTrader.df["close"].iloc[index-self.param_previous_bars]:
                flag = False

        new_flag = True
        
        if flag and new_flag:
            self.countdown += 1
            self.countdown_indices.append(self.tdSellSetup.sell_setup_index)

        if self.countdown >= self.param_countdown:
            self.checkCompletion(index)
        self.tdTrader.checkSellCountdownCancelation()
    
    def checkCompletion(self,index):
        if self.tdTrader.df["low"].iloc[index] >= self.tdTrader.df["close"].iloc[self.countdown_indices[self.param_bar_to_compare]]:
            flag = True
            for i in range(self.param_previous_bars):
                if self.tdTrader.df["close"].iloc[index] < self.tdTrader.df["close"].iloc[index-(i+1)]:
                    flag = False
            if flag:
                self.completed = True

    def cancelCountdown(self):
        self.canceled = True