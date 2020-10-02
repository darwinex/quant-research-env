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

class PredictiveDarwinAnalysis(object):

    def __init__(self):

        # Create the home variable:
        self.homeStr = os.path.expandvars('${HOME}')

    def _generateAnalysis(self, darwins):

        # Loop for each historical scores csv:
        for eachDarwin in darwins:

            logger.warning(f'Looping for DARWIN <{eachDarwin}>...')

            # Get the scores:
            SCORES = pd.read_csv(self.CSV_PATH + f'scoresData_{eachDarwin}.csv', index_col=0, parse_dates=True)
            logger.warning(SCORES.head(15))

            # Get the returns:
            RETURNS = pd.read_csv(self.CSV_PATH + f'returnsData_{eachDarwin}.csv', index_col=0, parse_dates=True)
            logger.warning(RETURNS.head(15))

            # Plot it:
            #self._plotInvAttsAndDarwinReturns(eachDarwin, RETURNS, SCORES, showIt=False)
            self._plotInvAttsAndDarwinReturns(eachDarwin, RETURNS, SCORES, showIt=True)

    def _plotInvAttsAndDarwinReturns(self, darwinString, returnsDF, scoresDF, showIt=True):

        # Get first index value so that we match available data:
        firstDate = returnsDF.index[0]

        # For each investment attribute, generate a plot:
        for eachAttributeName in scoresDF.columns:

            # Set figure and axis:
            f1, ax = plt.subplots(figsize = (10,5))
            f1.canvas.set_window_title(eachAttributeName)

            # Plot returns of candles + attributes:
            plt.plot(scoresDF.loc[firstDate:, eachAttributeName], label=eachAttributeName)
            plt.plot(returnsDF[f'{darwinString}_returns'], label=f'Weekly Returns {darwinString}')

            # Settle other stuff:
            plt.grid(linestyle='dotted')
            plt.xlabel('Observations')
            plt.ylabel('Values')
            plt.title(f'Inv Att ({eachAttributeName}) + Weekly Returns of Darwin <{darwinString}>')
            plt.legend(loc='best')
            plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

            # Show it:
            if showIt: 
                plt.show()

            # Close each plot:
            plt.close()

    def _executeQuantAnalysis(self):

        # Get historical scores for csvs:
        DARWINS = ['LVS', 'THA']
        #self.CSV_PATH = f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/Data/Daily/'
        #self.CSV_PATH = f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/Data/Weekly/'
        self.CSV_PATH = f'{self.homeStr}/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/Data/Monthly/'

        # Generate analysis (plots, csvs...):
        self._generateAnalysis(DARWINS)

if __name__ == "__main__":

    # Get it:
    ANALYSIS = PredictiveDarwinAnalysis()

    # New methods:
    ANALYSIS._executeQuantAnalysis()