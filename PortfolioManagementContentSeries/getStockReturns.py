# First, we append the previous level to the sys.path var:
import sys, os
# We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Import the logger:
import logging, time, json, random, pickle
import pandas as pd, numpy as np
from datetime import datetime
logger = logging.getLogger()

# Import plotting things:
import matplotlib.pyplot as plt

class QuantitativePortfolioManagement(object):

    def __init__(self):

        # Let's create the auth credentials:
        self.homeStr = os.path.expandvars('${HOME}')

    def _createStockPortfolio(self, timeframe):

        # Get stocks:
        dataPath = f'{self.homeStr}/Desktop/Darwinex/quant-research-env/PortfolioManagementContentSeries/Data/stocksCloseData_{timeframe}.csv'
        STOCKS_DATA = pd.read_csv(dataPath, index_col=0)
        STOCKS_DATA.dropna(axis=0, inplace=True)

        # Return it:
        logger.warning(STOCKS_DATA)
        return STOCKS_DATA

    def _saveReturnsDataFrame(self, DF_CLOSE, timeframe):

        # Generate log returns for each column:
        DF_RETURNS = DF_CLOSE.copy()

        # Loop:
        for eachColumn in DF_CLOSE:

            # Generate new columns for log returns:
            DF_RETURNS[f'{eachColumn}_returns'] = np.log(DF_CLOSE[eachColumn]/DF_CLOSE[eachColumn].shift(1))
            # Generate new columns for raw returns:
            #DF_RETURNS[f'{eachColumn}_returns'] = DF_CLOSE[eachColumn].pct_change()

        # Drop NaNs:
        DF_RETURNS.dropna(axis=0, inplace=True)

        # Save it to csv:
        DF_RETURNS.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/PortfolioManagementContentSeries/Data/returnsData_{timeframe}.csv')
    
    def _executeQuantAnalysis(self):

        # Get historical scores for darwins from the API:
        timeframeList = ['Daily', 'Weekly', 'Monthly']

        for eachTimeFrame in timeframeList:

            # Load the data:
            HIST_DATA = self._createStockPortfolio(eachTimeFrame)

            # Generate returns:
            self._saveReturnsDataFrame(HIST_DATA, eachTimeFrame)

if __name__ == "__main__":

    # Get it:
    ANALYSIS = QuantitativePortfolioManagement()

    # New methods:
    ANALYSIS._executeQuantAnalysis()