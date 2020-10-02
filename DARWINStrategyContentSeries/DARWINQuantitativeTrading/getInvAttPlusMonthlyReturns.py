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

    '''https://help.darwinex.com/world-of-darwinex#investment-attributes'''

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
        self.ACCOUNT_API = DWX_AccInfo_API(self.AUTH_CREDS, _version=2.0, _demo=isDemo)
        self.TRADING_API = DWX_Trading_API(self.AUTH_CREDS, _version=1.1, _demo=isDemo)

    def _assertRequestResponse(self, response):

        # Print response:
        logger.warning(response)

    ######################################## Auxiliary methods ########################################

    ######################################## Quantitative Analysis Methods ########################################

    def _getDarwinClosesDataFrame(self, response, darwinSymbol):

        # Filter the dictionary and just get the close:
        self.newDict = {key : value['close'] for key, value in response.items()}

        # Convert to dataframe:
        DF_CLOSE = pd.DataFrame.from_dict(self.newDict)

        # Generate log returns for each column:
        DF_RETURNS = DF_CLOSE.copy()

        # Resample to weekly and monthly values > We are already getting candles for weeks/months!
        # NOTE: Need to get daily and rebalance, because we get different dates in 
        DF_RETURNS = DF_RETURNS.resample('M').last().dropna()

        # Loop:
        for eachColumn in DF_CLOSE:

            # Generate new columns for log returns:
            DF_RETURNS[f'{eachColumn}_returns'] = np.log(DF_RETURNS[eachColumn]/DF_RETURNS[eachColumn].shift(1))
            # Generate new columns for raw returns:
            #DF_RETURNS[f'{eachColumn}_returns'] = DF_RETURNS[eachColumn].pct_change()

            # NOTE: Change negative returns (we cannot go short on DARWINs) for zero values:
            # We will get zeros in the returnsData.csv because of that!
            DF_RETURNS[DF_RETURNS < 0] = 0

        # Drop NaNs:
        DF_RETURNS.dropna(axis=0, inplace=True)
        DF_RETURNS.dropna(axis=1, inplace=True)

        # Save it to csv:
        DF_RETURNS.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/Data/Monthly/returnsData_{darwinSymbol[0]}.csv')

        # Return it:
        return DF_RETURNS

    def _generateAnalysis(self, historicalDarwinScores):

        # Loop for each darwin + scores dataframe:
        for eachDarwin, eachScoresDf in historicalDarwinScores.items():

            logger.warning(f'Looping for DARWIN <{eachDarwin}>...')

            # Just get dataframe from certain columns:
            eachScoresDf = eachScoresDf[['Rs', 'Os', 'Cs', 'Rp', 'Rm', 'Dc', 'La', 'Pf', 'Cp', 'Ds']]

            # Resample to weekly and monthly values:
            eachScoresDf = eachScoresDf.resample('M').last().dropna()

            # Apply log returns for every column and create new DF:
            dataFrameReturns = pd.DataFrame()

            # Loop:
            for eachColumn in eachScoresDf:
                dataFrameReturns[f'{eachColumn}_returns'] = np.log(eachScoresDf[eachColumn]/eachScoresDf[eachColumn].shift(1))

            # Save it to csv:
            dataFrameReturns.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/Data/Monthly/scoresData_{eachDarwin}.csv')

            # Plot it:
            self._plotInvAttsAndDarwinReturns(eachDarwin, dataFrameReturns, showIt=False)
            #self._plotInvAttsAndDarwinReturns(eachDarwin, dataFrameReturns, showIt=True)

    def _plotInvAttsAndDarwinReturns(self, darwinString, invAttDataframe, showIt=True):

        # Get the candles for that darwin:
        CLOSE_DF = self._createCandlePortfolio(symbol=[darwinString])

        # Get first index value so that we match available data:
        firstDate = CLOSE_DF.index[0]

        # For each investment attribute, generate a plot:
        for eachAttributeName in invAttDataframe.columns:

            # Set figure and axis:
            f1, ax = plt.subplots(figsize = (10,5))
            f1.canvas.set_window_title(eachAttributeName)

            # Plot returns of candles + attributes:
            plt.plot(invAttDataframe.loc[firstDate:, eachAttributeName], label=eachAttributeName)
            plt.plot(CLOSE_DF[f'{darwinString}_returns'], label=f'Monthly Returns {darwinString}')

            # Settle other stuff:
            plt.grid(linestyle='dotted')
            plt.xlabel('Observations')
            plt.ylabel('Values')
            plt.title(f'Inv Att ({eachAttributeName}) + Monthly Returns of Darwin <{darwinString}>')
            plt.legend(loc='best')
            plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

            # In PNG:
            filePath = f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/Plots/Monthly/'
            plt.savefig(filePath + f'PNGFormat/{eachAttributeName}_{darwinString}.png')

            # In pickle:
            with open(filePath + f'PickleFormat/{eachAttributeName}_{darwinString}.pickle', 'wb') as pickleFile:
                pickle.dump(f1, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)

            # Show it:
            if showIt: 
                plt.show()

            # Close each plot:
            plt.close()

    ######################################## Quantitative Analysis Methods ########################################

    ######################################## Data API ########################################
    
    def _createCandlePortfolio(self, symbol):

        # Get DARWINs:
        RETURNED_RESPONSE = self.INFO_API._Get_DARWIN_OHLC_Candles_(_symbols=symbol,
                                                                    _resolution='1d', # 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1m
                                                                    _from_dt='',
                                                                    _to_dt=str(pd.Timestamp('now')),
                                                                    _timeframe='/2Y', # 1D, 1W, 1M, 3M, 6M, 1Y, 2Y, ALL
                                                                    _delay=1.0) 
        self._assertRequestResponse(RETURNED_RESPONSE)

        # Create a dataframe with just the close of each DARWIN:
        RETURNED_RESPONSE = self._getDarwinClosesDataFrame(RETURNED_RESPONSE, symbol)
        
        # Return it:
        return RETURNED_RESPONSE

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

    def _createHistoricalScores(self, filteredDarwinsSymbols):

        # Get historical quotes:
        RETURNED_RESPONSE = self.INFO_API._Get_Historical_Scores_(_symbols=filteredDarwinsSymbols,
                                                                  _delay=1.0)

        # Print it:
        self._assertRequestResponse(RETURNED_RESPONSE)

        # Return it:
        return RETURNED_RESPONSE

    ######################################## Data API ########################################

    def _executeQuantAnalysis(self):

        # Set how many DARWINs we want to get:
        howMany = 2

        ########################

        # ALL AND FILTER ON QUANTITY:
        #FILTERED_DARWINS = self._createAllDARWINsPortfolio(howMany=howMany)

        # FILTER ON INVESTMENT ATT VALUES:
        #FILTERED_DARWINS = self._createInvestmentAttrsFilteredPortfolio(howMany=howMany)

        # JUST SOME SYMBOLS TO TEST:
        FILTERED_DARWINS = ['LVS', 'THA']

        ########################

        # Get historical scores for darwins from the API:
        HIST_SCORES = self._createHistoricalScores(filteredDarwinsSymbols=FILTERED_DARWINS)

        # Generate analysis (plots, csvs...):
        self._generateAnalysis(HIST_SCORES)

if __name__ == "__main__":

    # Get the credentials:
    from APICredentials import APICredentials
    AUTH_CREDENTIALS = APICredentials

    # Get it:
    ANALYSIS = QuantitativeDarwinAnalysis(AUTH_CREDENTIALS)

    # New methods:
    ANALYSIS._executeQuantAnalysis()