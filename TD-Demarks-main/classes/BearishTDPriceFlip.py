class BearishTDPriceFlip:
    def __init__(self,tdBuySetup, index, parameters):
        self.tdBuySetup = tdBuySetup
        self.index = index
        self.param1 = parameters["param1"]
        self.active = False

    def checkBearishTDPriceFlip(self):
        if self.index>self.param1 and self.index>self.param2:
            current_close = self.tdBuySetup.tdTrader.df.loc[self.index,"close"]
            previous_close_param1 = self.tdBuySetup.tdTrader.df.loc[self.index - self.param1 - 1, 'close'].value
            previous_close_after_param1 = self.tdBuySetup.tdTrader.df.loc[self.index - self.param1, 'close'].value

            if previous_close_param1 <= current_close:
                self.active = False
                return False 
            if previous_close_after_param1 >= current_close:
                self.active = False
                return False 
            
        self.active = True
        return True