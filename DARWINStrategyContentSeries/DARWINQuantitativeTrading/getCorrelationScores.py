# First, we append the previous level to the sys.path var:
import sys, os
# We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Import the different classes:
from darwinexapis.API.DarwinDataAnalyticsAPI.DWX_Data_Analytics_API import DWX_Darwin_Data_Analytics_API
from darwinexapis.API.InfoAPI.DWX_Info_API import DWX_Info_API
from darwinexapis.API.TradingAPI.DWX_Trading_API import DWX_Trading_API
from darwinexapis.API.InvestorAccountInfoAPI.DWX_AccInfo_API import DWX_AccInfo_API

# Import the logger:
import logging, time, json, random, pickle
import pandas as pd, numpy as np
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from datetime import datetime
logger = logging.getLogger()

### Import plotting things:
import matplotlib.pyplot as plt
import seaborn as sn

class PredictiveDarwinAnalysis(object):

    def __init__(self, authCreds):

        ### Let's create the auth credentials:
        self.AUTH_CREDS = authCreds
        self.homeStr = os.path.expandvars('${HOME}')

        # Create the objects:
        self._defineAPIObjects()

    #########################################

    def _defineAPIObjects(self, isDemo=True):

        # Get the other APIs:
        self.INFO_API = DWX_Info_API(self.AUTH_CREDS, _version=2.1, _demo=isDemo)
        self.ACCOUNT_API = DWX_AccInfo_API(self.AUTH_CREDS, _version=2.0, _demo=isDemo)
        self.TRADING_API = DWX_Trading_API(self.AUTH_CREDS, _version=1.1, _demo=isDemo)

    def _assertRequestResponse(self, response):

        # Print response:
        logger.warning(response)

    #########################################

    def _plotCorrelationMatrix(self, closesDF):

        # Generate correlation matrix and plot:
        # We make it with the closes to get also negative values.
        logger.warning(closesDF.head())
        DF_CORR = closesDF.corr()
        DF_CORR_ABS = closesDF.corr().abs()
        closesDF.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/CorrelationStudies/corrData.csv')
        DF_CORR.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/CorrelationStudies/corrMatrix.csv')

        # Plot:
        ax = sn.heatmap(DF_CORR, annot=True, center=0, linewidths=.5, cmap='icefire') # cmap='coolwarm'

        # Settle other stuff:
        plt.title('Correlation Matrix')
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

        # Save it
        # In PNG:
        filePath = f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/CorrelationStudies/'
        plt.savefig(filePath + 'correlationMatrix.png')

        # In pickle:
        f1 = ax.get_figure()
        f1.canvas.set_window_title('Correlation Matrix')
        with open(filePath + 'correlationMatrix.pickle', 'wb') as pickleFile:
            pickle.dump(f1, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)

        # Show it:
        plt.show()

        # Return the corr matrix:
        return DF_CORR, DF_CORR_ABS

    #########################################

    def _createAllDARWINsPortfolio(self, howMany=None):

        # Get filtered DARWINs:
        RETURNED_RESPONSE = self.INFO_API._Get_DARWIN_Universe_(_status='ACTIVE',
                                                                _page=0,
                                                                _perPage=1000,
                                                                _iterate=True,
                                                                _delay=1.0)

        self._assertRequestResponse(RETURNED_RESPONSE)

        # Get the symbols and delete the suffix:
        FILTERED_DARWIN_SYMBOLS = RETURNED_RESPONSE['shortName'].to_list()
        print(f'QUANTITY OF DARWINS THAT ARE ACTIVE: {len(FILTERED_DARWIN_SYMBOLS)}')

        # Filter:
        if howMany:
            FILTERED_DARWIN_SYMBOLS = random.sample(FILTERED_DARWIN_SYMBOLS, howMany)

        # Return it:
        return FILTERED_DARWIN_SYMBOLS

    def _createInvestmentAttrsFilteredPortfolio(self, howMany):

        # Get filtered DARWINs:
        RETURNED_RESPONSE = self.INFO_API._Get_Filtered_DARWINS_(_filters=[['Cs', 8, 10, 'actual'],
                                                                           ['Mc', 8, 10, 'actual'],
                                                                           ['La', 8, 10, 'actual'],
                                                                           ['days_in_darwinex', 40, 100, 'actual']],
                                                                _order=['dScore','1m','DESC'], # DESC, ASC
                                                                _page=0, # Sets the page we want to start from
                                                                _perPage=50, # Sets the items per page we want to get
                                                                _delay=1.0)
        self._assertRequestResponse(RETURNED_RESPONSE)

        # It is suppossed to return a dataframe althoguh emptys:
        if RETURNED_RESPONSE.empty:
            print('No DARWIN satisfies the criteria')
            
        else:

            # Get the symbols and delete the suffix:
            FILTERED_DARWIN_SYMBOLS = RETURNED_RESPONSE['productName'].to_list()[:howMany]
            FILTERED_DARWIN_SYMBOLS = [eachSymbol.split('.')[0] for eachSymbol in FILTERED_DARWIN_SYMBOLS]

            # Return it:
            return FILTERED_DARWIN_SYMBOLS

    #########################################

    def _createCandlePortfolio(self, symbols):

        # Get DARWINs:
        RETURNED_RESPONSE = self.INFO_API._Get_DARWIN_OHLC_Candles_(_symbols=symbols,
                                                                    _resolution='1d', # 1w, 1mn
                                                                    _from_dt='',
                                                                    _to_dt=str(pd.Timestamp('now')),
                                                                    _timeframe='/1M', # 1D, 1W, 1M, 3M, 6M, 1Y, 2Y, ALL
                                                                    _delay=1.0) 
        self._assertRequestResponse(RETURNED_RESPONSE)

        # Create a dataframe with just the close of each DARWIN:
        RETURNED_RESPONSE = self._getDarwinClosesDataFrame(RETURNED_RESPONSE)
        
        # Return it:
        return RETURNED_RESPONSE

    def _getDarwinClosesDataFrame(self, response):

        # Filter the dictionary and just get the close:
        self.newDict = {key : value['close'] for key, value in response.items()}

        # Convert to dataframe:
        DF_CLOSE = pd.DataFrame.from_dict(self.newDict)

        # Drop NaNs:
        DF_CLOSE.dropna(axis=0, inplace=True)
        DF_CLOSE.dropna(axis=1, inplace=True)

        # Return it:
        return DF_CLOSE

    #########################################

    def _checkForLowCorrelation(self, absCorrMatrix):

        # Sort them and get the lowest:
        corrMatrixUnstacked = absCorrMatrix.unstack()
        sortedCorrMatrix = corrMatrixUnstacked.sort_values(kind="quicksort")

        return sortedCorrMatrix

    def _findLessCorrelatedDARWINs(self, howManyToTest=4, howManyToTrade=5):

        # Get X DARWINs:
        #DARWINS_SYMBOLS = self._createAllDARWINsPortfolio(howMany=howManyToTest)

        # FILTER ON INVESTMENT ATT VALUES:
        # DARWINS_SYMBOLS = self._createInvestmentAttrsFilteredPortfolio(howMany=howManyToTest)

        # JUST SOME OF THEM:
        DARWINS_SYMBOLS = ['LVS', 'THA', 'OOS', 'PLF', 'CIS', 'KLG', 'SYO', 'JHU']
        logger.warning(DARWINS_SYMBOLS)

        # Get candles for those DARWINs:
        CANDLES_CLOSE_DARWINS = self._createCandlePortfolio(DARWINS_SYMBOLS)
        logger.warning(CANDLES_CLOSE_DARWINS)

        # Check for correlation:
        CORRELATION_MATRIX, ABS_CORRELATION_MATRIX = self._plotCorrelationMatrix(CANDLES_CLOSE_DARWINS)
        logger.warning(CORRELATION_MATRIX)

        # Find less correlated ones:
        LESS_CORRELATED = self._checkForLowCorrelation(ABS_CORRELATION_MATRIX)
        logger.warning('LESS CORRELATED DARWINS:')
        logger.warning(LESS_CORRELATED)

    ##########################################################

    def _executeQuantAnalysis(self):

        # ALL AND FILTER ON QUANTITY:
        self._findLessCorrelatedDARWINs()

if __name__ == "__main__":

    # Get the credentials:
    from APICredentials import APICredentials
    AUTH_CREDENTIALS = APICredentials

    # Get it:
    ANALYSIS = PredictiveDarwinAnalysis(AUTH_CREDENTIALS)

    # New methods:
    ANALYSIS._executeQuantAnalysis()