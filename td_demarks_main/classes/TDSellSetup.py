from td_demarks_main.classes.BullishTDPriceFlip import BullishTDPriceFlip

class TDSellSetup:
    def __init__(self, tdTrader, index, parameters):
        self.tdTrader = tdTrader
        self.index = index
        self.param_consecutive = parameters["TDBuySetup"]["param_consecutive"]
        self.param_earlier = parameters["TDBuySetup"]["param_earlier"]
        self.param_bullish_td_price_flip = parameters["BullishTDPriceFlip"]
        self.param_perfection = parameters["TDSellSetup"]["param_perfection"] #int: number of consecutive bars to compare, e.g. if it is 2 then it will compare the last two bars with the two bars before (the same happens for other values)

        self.count = 0
        self.active = False
        self.sell_setup = False #TDSell
        self.sell_setup_index = -1 #comleted TDSellSetup index 

        self.perfection = False #TDSellSetup Perfection
        self.minimum = None
        self.maximum = None
        
    def checkBullishTDPriceFlip(self,index):
        bullishTDPF = BullishTDPriceFlip(self, index,self.param_bullish_td_price_flip)
        self.active = bullishTDPF.checkBullishTDPriceFlip()
    
    def checkTDSellSetup(self,index):
        current_close = self.tdTrader.df["close"].iloc[index]
        current_low = self.tdTrader.df["low"].iloc[index]
        current_high = self.tdTrader.df["high"].iloc[index]

        previous_close = self.tdTrader.df.loc[-self.param_earlier + index, 'close'].value
        if current_close <= previous_close:
            self.active = False
            self.count = 0
            self.sell_setup = False

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
            self.sell_setup = True
            self.sell_setup_index = self.index + self.count
            self.checkTDSellPerfection()

    def checkTDSellPerfection(self,index):
        """
        This checks perfection without a subsequent low after the TDBuySetup. 
        That needs to be done in the TDTrader
        """
        self.perfection = False
        for i in range(self.param_perfection):
            count = 0
            for ii in range(self.param_perfection):
                if self.tdTrader.df["low"].iloc[-index-i] <= self.tdTrader.df["low"].iloc[-index-self.param_perfection-ii]:
                    break
                count +=1
            if count == self.param_perfection:
                self.perfection = True
                return None
            
    def updateInformation(self,index):
        if self.active:
            self.count += 1
            self.checkTDSellSetup(index)

        if not self.active:
            self.checkBullishTDPriceFlip(index)
            self.index = index