# First, we append the previous level to the sys.path var:
import sys, os
# We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Import the logger:
import logging, time, json, random, pickle, itertools
import pandas as pd, numpy as np
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from datetime import datetime
logger = logging.getLogger()

# Import plotting things:
import matplotlib.pyplot as plt
import seaborn as sn

class CorrelationStudies(object):

    def __init__(self):

        # Let's fix some parameters:
        self.homeStr = os.path.expandvars('${HOME}')

    def _createStockPortfolio(self, timeframe, howMany):

        # Get stocks:
        dataPath = f'{self.homeStr}/Desktop/Darwinex/quant-research-env/PortfolioManagementContentSeries/Data/stocksCloseData_{timeframe}.csv'
        STOCKS_DATA = pd.read_csv(dataPath, index_col=0)
        self.stockSymbolsList = list(STOCKS_DATA.columns)
        STOCKS_DATA.dropna(axis=0, inplace=True)

        # Get just some stocks for trial:
        STOCKS_DATA = STOCKS_DATA[list(STOCKS_DATA.columns)[:howMany]]

        # Return it:
        logger.warning(STOCKS_DATA)
        return STOCKS_DATA

    def _getLowestCorrPortfolio(self, corrMatrix, stockSymbols):

        # Get combinations up to X assets:
        stockPortCombinations = list(itertools.combinations(stockSymbols, 6))
        logger.warning(stockPortCombinations)

        # Create placeholders:
        portfoliosDict = {}
        corrDict = {}
        corrDictAbs = {}

        # Loop:
        for eachPortfolioIteration, eachCombination in enumerate(stockPortCombinations, 1):

            # Set:
            corrValueFinal = 0
            logger.warning(f'POSSIBLE PORTFOLIO: {eachCombination}')
            logger.warning(f'CORR VALUE FINAL (PRE-LOOP): {corrValueFinal}')

            # Create comparable pairs:
            stockPairs = list(itertools.combinations(eachCombination, 2))

            # Loop and add:
            for eachStockPair in stockPairs:

                # Get the corr value and add:
                corrValue = corrMatrix.loc[eachStockPair[0], eachStockPair[1]]
                corrValueFinal += corrValue

            # Print value final:
            logger.warning(f'CORR VALUE FINAL (AFTER LOOP): {corrValueFinal}')

            # Fill:
            portfoliosDict[eachPortfolioIteration] = eachCombination
            corrDict[eachPortfolioIteration] = corrValueFinal
            corrDictAbs[eachPortfolioIteration] = abs(corrValueFinal)
        
        # Get the key:
        minKey = min(corrDict, key=corrDict.get)
        minKeyNearZero = min(corrDictAbs, key=corrDictAbs.get)

        return corrDict[minKey], portfoliosDict[minKey], corrDictAbs[minKeyNearZero], portfoliosDict[minKeyNearZero]

    def _plotCorrelationMatrix(self, closesDF, eachTimeFrame):

        # Generate correlation matrix and plot > We make it with the closes to get also negative values.
        logger.warning(closesDF.head())
        DF_CORR = closesDF.corr()
        DF_CORR_ABS = closesDF.corr().abs()
        closesDF.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/PortfolioManagementContentSeries/CorrelationStudies/corrData_{eachTimeFrame}.csv')
        DF_CORR.to_csv(f'{self.homeStr}/Desktop/Darwinex/quant-research-env/PortfolioManagementContentSeries/CorrelationStudies/corrMatrix_{eachTimeFrame}.csv')

        # Plot:
        ax = sn.heatmap(DF_CORR, annot=True, center=0, linewidths=.5, cmap='icefire') # cmap='coolwarm'

        # Settle other stuff:
        plt.title('Correlation Matrix')
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

        # Save it
        # In PNG:
        filePath = f'{self.homeStr}/Desktop/Darwinex/quant-research-env/PortfolioManagementContentSeries/CorrelationStudies/'
        plt.savefig(filePath + f'correlationMatrix_{eachTimeFrame}.png')

        # In pickle:
        f1 = ax.get_figure()
        f1.canvas.set_window_title('Correlation Matrix')
        with open(filePath + f'correlationMatrix_{eachTimeFrame}.pickle', 'wb') as pickleFile:
            pickle.dump(f1, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)

        # Show it:
        plt.show()

        # Return the corr matrix:
        return DF_CORR, DF_CORR_ABS

    def _findLessCorrelatedStocks(self):

        timeframeList = ['Daily', 'Weekly', 'Monthly']

        for eachTimeFrame in timeframeList:

            # Load the data:
            HIST_DATA = self._createStockPortfolio(eachTimeFrame, howMany=20)

            # Check for correlation:
            CORRELATION_MATRIX, ABS_CORRELATION_MATRIX = self._plotCorrelationMatrix(HIST_DATA, eachTimeFrame)
            logger.warning(CORRELATION_MATRIX)

            # Find less correlated ones:
            LESS_CORR_MINUS, LESS_CORR_PORT_MINUS, LESS_CORR_ZERO, LESS_CORR_PORT_ZERO = self._getLowestCorrPortfolio(CORRELATION_MATRIX, 
                                                                                                                      list(HIST_DATA.columns))
            logger.warning('#####################################')
            logger.warning('LESS CORRELATED VALUE (MINUS):')
            logger.warning(LESS_CORR_MINUS)
            logger.warning('LESS CORRELATED PORTFOLIO (MINUS):')
            logger.warning(LESS_CORR_PORT_MINUS)
            logger.warning('LESS CORRELATED VALUE (NEAR ZERO):')
            logger.warning(LESS_CORR_ZERO)
            logger.warning('LESS CORRELATED PORTFOLIO (NEAR ZERO):')
            logger.warning(LESS_CORR_PORT_ZERO)
            logger.warning('#####################################')

if __name__ == "__main__":

    # Get it:
    ANALYSIS = CorrelationStudies()

    # New methods:
    ANALYSIS._findLessCorrelatedStocks()