class BullishTDPriceFlip:
    def __init__(self, tdSellSetup, index, parameters):
        self.tdSellSetup = tdSellSetup
        self.index = index
        self.param1 = parameters["param1"]
        self.param2 = parameters["param2"]
        self.active = False
        

    def checkBullishTDPriceFlip(self):
        if self.index>self.param1 and self.index>self.param2:
            current_close = self.tdSellSetup.tdTrader.df.loc[self.index,"close"]
            previous_close_param1 = self.tdSellSetup.tdTrader.df.loc[self.index-self.param1-1, 'close'].value
            previous_close_param2 = self.tdSellSetup.tdTrader.df.loc[self.index-self.param1, 'close'].value

            if previous_close_param1 >= current_close:
                self.active = False
                return False 
            if previous_close_param2 <= current_close:
                self.active = False
                return False 
            
        self.active = True
        return True