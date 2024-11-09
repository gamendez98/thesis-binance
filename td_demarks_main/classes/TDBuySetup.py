from td_demarks_main.classes.BearishTDPriceFlip import BearishTDPriceFlip

class TDBuySetup:
    def __init__(self, tdTrader, index, parameters):
        self.tdTrader = tdTrader
        self.index = index #index of the dataframe at which the bearishTDPriceFlip is calculated
        self.param_consecutive = parameters["TDComboBuySetup"]["param_consecutive"] #int
        self.param_earlier = parameters["TDComboBuySetup"]["param_earlier"] #int
        self.param_bearish_td_price_flip = parameters["BearishTDPriceFlip"] #dic
        self.count = 0
        self.active = False
        self.buy_setup = False #TDBuySetup
        self.buy_setup_index = -1 #comleted TDBuySetup index 
        self.perfection = False #TDBuySetup Perfection
        self.minimum = None
        self.maximum = None
       
        
    def checkBearishTDPriceFlip(self,index):
        bearishTDPF = BearishTDPriceFlip(self,index,self.param_bearish_td_price_flip)
        if bearishTDPF.checkBearishTDPriceFlip():
            if self.checkTDBuySetup(index):
                self.active = True
                self.count += 1
                self.bearishTDPriceFlip = bearishTDPF
    
    def checkTDBuySetup(self,index):
        current_close = self.tdTrader.df["close"].iloc[index]
        current_low = self.tdTrader.df["low"].iloc[index]
        current_high = self.tdTrader.df["high"].iloc[index]

        previous_close = self.tdTrader.df.loc[-self.param_earlier + index, 'close'].value

        if current_close>=previous_close:
            self.active = False
            self.count = 0
            self.buy_setup = False
            self.perfection = False
            return False
        
        if self.minimum == None:
            self.minimum = current_low
        else:
            if current_low < self.minimum:
                self.minimum = current_low

        if self.maximum == None:
            self.maximum = current_high
        else:
            if current_high < self.maximum:
                self.maximum = current_high

        if self.count == self.param_consecutive:
            self.buy_setup = True
            self.buy_setup_index = self.index + self.count
            self.checkTDBuyPerfection(self,index)
        
        return True

    def updateInformation(self,index): #Returns True if the setup is completed and False else.
        if not self.active:
            self.checkBearishTDPriceFlip()
            self.index = index
            return False
        
        if self.active:
            self.count += 1
            self.checkTDBuySetup(self,index)
            if self.buy_setup == True:
                return True
            else:
                return False