# Imports:
import yfinance as yf # pip install yfinance
import pandas as pd
import os

class StockData(object):

    def __init__(self):

        # Define the stock string and parameters:
        self.stocksString = "AAL AAPL ADBE ADI ADP ADSK ALXN AMAT AMD AMGN AMZN ATVI AVGO BIIB BKNG CHTR CMCSA CME COST CSX CTSH DLTR EA EBAY EXPE FAST FB FISV FITB GILD GOOG GOOGL ILMN INTC INTU ISRG KHC KLAC LRCX MAR MCHP MDLZ MSFT MU NFLX NTAP NVDA ORLY PEP PYPL QCOM REGN ROST SBUX SPLK SWKS TMUS TSLA TTWO TXN ULTA VRTX WBA WDAY WDC XLNX ABBV ABT ACN ADM AEP AIG ALL AMT ANTM APD AXP BA BAC BAX BBY BDX BK BLK BMY BSV C CAH CAT CB CCI CCL CI CL CLX CMA CMI CNC COF COP CRM CVS CVX CXO D DAL DD DE DFS DG DHI DHR DIS DUK EL EMR EOG ETN EW EXC FDX FIS FTV GD GE GIS GLW GM GS GWW HAL HCA HD HES HLT HON HPE HPQ HUM IBM ICE ITW JCI JNJ JPM KDP KEY KMB KMI KO KR LEN LLY LMT LOW LUV LVS LYB MA MCD MCK MDT MET MMC MMM MO MPC MRK MS NEE NEM NKE NOC NSC OKE OMC ORCL OXY PANW PFE PG PGR PH PLD PM PNC PPG PRU PSA PXD RCL RF ROK SCHW SHW SLB SO SPG SPGI SRE STT STZ SWK SYF SYK SYY T TGT TJX TMO TRV TSN TWTR UAL UNH UNP UPS USB V VFC VLO VMW VZ WFC WM WMB WMT XOM ZTS"
        self.periodOfData = '2y'
        self.intervalOfData = '1d'
        self.columnToRetrieve = 'Adj Close'
        self.homeStr = os.path.expandvars('${HOME}')

        # Call the method:
        self._getData()

    def _getData(self):

        # Get the data:
        DATA = yf.download(self.stocksString,                    
                           period=self.periodOfData,
                           interval=self.intervalOfData,
                           group_by='ticker')

        # Filter the dictionary and just get the close:
        newDict = {stockSymbol : DATA[stockSymbol][self.columnToRetrieve] for stockSymbol, dataFrameColumn in DATA if dataFrameColumn == self.columnToRetrieve}

        # Convert to dataframe:
        DF_CLOSE = pd.DataFrame.from_dict(newDict)

        # Save it:
        DF_CLOSE.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/PortfolioManagementContentSeries/Data/stocksCloseData_Daily.csv')

        # Convert:
        self._convertToWeeklyData(DF_CLOSE)
        self._convertToMonthlyData(DF_CLOSE)

    def _convertToWeeklyData(self, data):

        # Make a copy:
        df = data.copy()

        # Convert and save:
        df = df.resample('W').last()
        df.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/PortfolioManagementContentSeries/Data/stocksCloseData_Weekly.csv')

    def _convertToMonthlyData(self, data):

        # Make a copy:
        df = data.copy()

        # Convert and save:
        df = df.resample('M').last()
        df.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/PortfolioManagementContentSeries/Data/stocksCloseData_Monthly.csv')

if __name__ == "__main__":

    # Get it:
    ANALYSIS = StockData()