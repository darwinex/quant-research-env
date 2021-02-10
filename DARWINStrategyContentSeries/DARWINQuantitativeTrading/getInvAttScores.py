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
import logging, time, json, random
import pandas as pd, numpy as np
from datetime import datetime
logger = logging.getLogger()

### Import plotting things:
import matplotlib.pyplot as plt

class GetInvestmentAttsScores(object):

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

    def _saveToCSVAndPlot(self, responseToSave):

        # Save it:
        for eachDarwin, eachScoresDf in responseToSave.items():

            # Just get dataframe from certain columns:
            eachScoresDf = eachScoresDf[['Rs', 'Os', 'Cs', 'Rp', 'Rm', 'Dc', 'La', 'Pf', 'Cp', 'Ds']]

            # Resample to weekly and monthly values:
            eachScoresDfResampled = eachScoresDf.resample('W').last().dropna()
            #eachScoresDfResampled = eachScoresDf.resample('M').last().dropna()

            eachScoresDfResampled.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/Data/scoresData_{eachDarwin}.csv')

        # Plot it:
        self._plotEachAttribute(responseToSave, showIt=False)
        #self._plotEachAttributeInSamePlot(responseToSave, showIt=False)

    def _plotEachAttribute(self, responseToPlot, showIt=True):

        # Plot:
        for eachDarwin, eachScoresDf in responseToPlot.items():

            for eachAttributeName in eachScoresDf.columns:

                f1, ax = plt.subplots(figsize = (10,5))
                f1.canvas.set_window_title('eachAttributeName')
                plt.plot(eachScoresDf[eachAttributeName], label=eachAttributeName)
                plt.grid(linestyle='dotted')
                plt.xlabel('Observations')
                plt.ylabel('Values')
                plt.title(f'Attribute: {eachAttributeName}')
                plt.legend(loc='best')
                plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

                # In PNG:
                plt.savefig(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/Plots/{eachAttributeName}_{eachDarwin}.png')

                # Show it:
                if showIt: 
                    plt.show()

                # Close each plot:
                plt.close()

    def _plotEachAttributeInSamePlot(self, responseToPlot, showIt=True):

        # NOTE: Doesn't work because dates don't match.

        f1, ax = plt.subplots(figsize = (10,5))

        # Plot:
        for eachDarwin, eachScoresDf in responseToPlot.items():

            # Resample to weekly and monthly values:
            eachScoresDfResampled = eachScoresDf.resample('W').last().dropna()
            print(eachScoresDfResampled.columns)
            #eachScoresDf = eachScoresDf.resample('M')
            print(eachScoresDfResampled.index)

            for eachAttributeName in eachScoresDfResampled.columns:

                # For each attribute in each dataframe, plot it:
                attributeName = eachAttributeName
                plt.title(f'Attribute: {attributeName}')
                plt.plot(eachScoresDfResampled.index, eachScoresDfResampled[attributeName], label=eachDarwin)

        # Other stuff:
        plt.grid(linestyle='dotted')
        plt.xlabel('Observations')
        plt.ylabel('Values')
        plt.legend(loc='best')
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

        # In PNG:
        plt.savefig(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/Plots/{attributeName}_Darwins.png')

        # Show it:
        if showIt: 
            plt.show()

        # Close each plot:
        plt.close()

    ######################################## Quantitative Analysis Methods ########################################

    ######################################## Analysis API ########################################

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

    ######################################## Analysis API ########################################

    def _getHistoricalScores(self):

        # Get darwin symbols:
        howMany = 5
        
        # ALL AND FILTER ON QUANTITY:
        FILTERED_DARWIN = self._createAllDARWINsPortfolio(howMany=howMany)

        # FILTER ON INVESTMENT ATT VALUES:
        #FILTERED_DARWIN = self._createInvestmentAttrsFilteredPortfolio(howMany=howMany)

        # Get historical quotes:
        RETURNED_RESPONSE = self.INFO_API._Get_Historical_Scores_(_symbols=FILTERED_DARWIN, #_symbols=['THA','LVS']
                                                                  _delay=1.0)

        # Do saving and printing:
        self._assertRequestResponse(RETURNED_RESPONSE)
        self._saveToCSVAndPlot(RETURNED_RESPONSE)

if __name__ == "__main__":

    # Get the credentials:
    AUTH_CREDENTIALS = {"access_token": "30d172b8-8a7f-320d-a393-b4e10f3a2a8a", "consumer_key": "Z4_p3FDLhI5x9pMlYWHvyiWW04Qa", "consumer_secret": "NR6hDOCbjJEfYzB2Hg1B9nfHhpAa", "refresh_token": "de926a00-ee73-34c9-a8f7-ebcd4dab266e"}

    # Get it:
    DASSETUNIVERSE = GetInvestmentAttsScores(AUTH_CREDENTIALS)
    
    # New methods:
    DASSETUNIVERSE._getHistoricalScores()