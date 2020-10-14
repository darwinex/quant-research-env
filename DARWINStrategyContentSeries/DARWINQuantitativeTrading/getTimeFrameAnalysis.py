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
from datetime import datetime
logger = logging.getLogger()

### Import plotting things:
import matplotlib.pyplot as plt

class QuantitativeDarwinAnalysis(object):

    def __init__(self, authCreds):

        ### Let's create the auth credentials:
        self.AUTH_CREDS = authCreds
        self.homeStr = os.path.expandvars('${HOME}')

        # Create the objects:
        self._defineAPIObjects()

    ######################################## Auxiliary methods ########################################

    def _defineAPIObjects(self, isDemo=True):

        # Get the other APIs:
        self.INFO_API = DWX_Info_API(self.AUTH_CREDS, _version=2.1, _demo=isDemo)

    def _assertRequestResponse(self, response):

        # Print response:
        logger.warning(response)

    ######################################## Auxiliary methods ########################################

    ######################################## Quantitative Analysis Methods ########################################

    def _getDarwinClosesDataFrame(self, response, darwinSymbol):

        # Resample to weekly and monthly values > We are already getting candles for weeks/months!
        offSetList = ['W', 'M', 'Y']

        # Filter the dictionary and just get the close:
        self.newDict = {key : value['close'] for key, value in response.items()}

        # Convert to dataframe:
        DF_CLOSE = pd.DataFrame.from_dict(self.newDict)

        for eachOffSet in offSetList:

            # Generate log returns for each column:
            DF_RETURNS = DF_CLOSE.copy()

            # Calculate:
            DF_RETURNS = DF_RETURNS.resample(eachOffSet).last().dropna()

            # Loop:
            for eachColumn in DF_CLOSE:

                # Generate new columns for log returns:
                #DF_RETURNS[f'{eachColumn}_returns'] = np.log(DF_RETURNS[eachColumn]/DF_RETURNS[eachColumn].shift(1))
                # Generate new columns for raw returns:
                DF_RETURNS[f'{eachColumn}_returns'] = DF_RETURNS[eachColumn].pct_change()

                # Drop NaNs:
                DF_RETURNS.dropna(axis=0, inplace=True)
                DF_RETURNS.dropna(axis=1, inplace=True)
                logger.warning(DF_RETURNS)

                winRate = 100. * (DF_RETURNS[f'{eachColumn}_returns'] >= 0).sum() / len(DF_RETURNS[f'{eachColumn}_returns'])
                logger.warning(f'WIN RATE FOR <{eachColumn}> (OFFSET > {eachOffSet}): {winRate}')

    ####################################### Quantitative Analysis Methods ########################################

    ######################################## Data API ########################################
    
    def _createCandlePortfolio(self, symbol):

        # Get DARWINs:
        RETURNED_RESPONSE = self.INFO_API._Get_DARWIN_OHLC_Candles_(_symbols=symbol,
                                                                    _resolution='1d', # 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1m
                                                                    _from_dt='',
                                                                    _to_dt=str(pd.Timestamp('now')),
                                                                    _timeframe='/6M', # 1D, 1W, 1M, 3M, 6M, 1Y, 2Y, ALL
                                                                    _delay=10.0)
        self._assertRequestResponse(RETURNED_RESPONSE)

        # Create a dataframe with just the close of each DARWIN:
        self._getDarwinClosesDataFrame(RETURNED_RESPONSE, symbol)

    def _createInvestmentAttrsFilteredPortfolio(self, howMany):

        # Get filtered DARWINs:
        RETURNED_RESPONSE = self.INFO_API._Get_Filtered_DARWINS_(_filters=[['Cs', 4, 10, 'actual'],
                                                                           ['Mc', 4, 10, 'actual'],
                                                                           ['La', 4, 10, 'actual'],
                                                                           ['days_in_darwinex', 400, 600, 'actual']],
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
        print(len(FILTERED_DARWIN_SYMBOLS))

        # Filter:
        if howMany:
            FILTERED_DARWIN_SYMBOLS = random.sample(FILTERED_DARWIN_SYMBOLS, howMany)

        # Return it:
        return FILTERED_DARWIN_SYMBOLS

    ######################################## Data API ########################################

    def _executeQuantAnalysis(self):

        # Set how many DARWINs we want to get:
        howMany = 40

        ########################

        # FILTER ON INVESTMENT ATT VALUES:
        FILTERED_DARWINS = self._createInvestmentAttrsFilteredPortfolio(howMany=howMany)

        # ALL AND FILTER ON QUANTITY:
        #FILTERED_DARWINS = self._createAllDARWINsPortfolio(howMany=howMany)
        #FILTERED_DARWINS = self._createAllDARWINsPortfolio(howMany=None)

        # JUST SOME SYMBOLS TO TEST:
        #FILTERED_DARWINS = ['LVS', 'THA', 'OOS', 'PLF', 'CIS', 'KLG', 'SYO', 'JHU', 'UYZ', 'BZC',
        #                    'ZVQ', 'JHU', 'SKI', 'UAE', 'BZC', 'KLG', 'SYO', 'JHU', 'UYZ', 'BZC',
        #                    'KLG', 'SYO', 'JHU', 'UYZ', 'BZC', 'KLG', 'SYO', 'JHU', 'UYZ', 'BZC',
        #                    'KLG', 'SYO', 'JHU', 'UYZ', 'BZC', 'KLG', 'SYO', 'JHU', 'UYZ', 'BZC',
        #                    'KLG', 'SYO', 'JHU', 'UYZ', 'BZC', 'KLG', 'SYO', 'JHU', 'UYZ', 'BZC']

        ########################

        # Get historical scores for darwins from the API:
        self._createCandlePortfolio(symbol=FILTERED_DARWINS)

if __name__ == "__main__":

    # Get the credentials:
    from APICredentials import APICredentials
    AUTH_CREDENTIALS = APICredentials

    # Get it:
    ANALYSIS = QuantitativeDarwinAnalysis(AUTH_CREDENTIALS)

    # New methods:
    ANALYSIS._executeQuantAnalysis()