# Imports:
from PortfolioClass import Portfolio
from AssetClass import Asset

# Import mlfinlab > pip install mlfinlab
from mlfinlab.data_structures import standard_data_structures
from mlfinlab.data_structures import get_ema_dollar_imbalance_bars, get_ema_tick_imbalance_bars, get_ema_volume_imbalance_bars
from mlfinlab.data_structures import get_ema_dollar_run_bars, get_ema_tick_run_bars, get_ema_volume_run_bars

# Import utils:
import os, glob, pprint
import numpy as np, pandas as pd

### Import plotting things:
import matplotlib.pyplot as plt
import seaborn as sns # pip install seaborn
from scipy.stats import norm, laplace, johnsonsu

### Set the style for the plots.
from matplotlib import style
style.use('dark_background')

class ResearchStudy(Portfolio):

    '''
    Formulates an hypothesis and tries to confirm in on a Portfolio object.
    Specifically, it will take some data from that portfolio, makes some calculations and returns a result
    '''

    def __init__(self, assetsList, formOrRead, sampleFormat='', dateHourString=''):

        # The generated data will be in PORTFOLIO._portfolioDict

        if formOrRead == 'form':

            self.PORTFOLIO = Portfolio(assetsList)
            self.PORTFOLIO._formPortfolioHistoricalData(sampleFormat)

        elif formOrRead == 'read':

            self.PORTFOLIO = Portfolio(assetsList)
            self.PORTFOLIO._readPortfolioHistoricalData(dateHourString)

    def _saveGeneratedDataFrames(self, saveDirectory):

        # Save each dataframe:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            print(f'[{self._generateLogReturns.__name__}] - Looping for asset <{eachAssetName}>...')
            eachAssetDataFrame.to_csv(saveDirectory + f'/{eachAssetName}_DF.csv')

    ######################### RETURNS #########################

    def _generateLogReturns(self):

        # Generates returns based on some metric.
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            print(f'[{self._generateLogReturns.__name__}] - Looping for asset <{eachAssetName}>...')
            eachAssetDataFrame['Returns'] = np.log(eachAssetDataFrame.close/eachAssetDataFrame.close.shift(1))
            eachAssetDataFrame.dropna(how='any', inplace=True)

    def _generateRawReturns(self):

        # Generates returns based on some metric.
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            print(f'[{self._generateRawReturns.__name__}] - Looping for asset <{eachAssetName}>...')
            eachAssetDataFrame['Returns'] = eachAssetDataFrame.close.pct_change()
            eachAssetDataFrame.dropna(how='any', inplace=True)

    def _generateMidPrice(self):

        # Loop for all the assets:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():
            eachAssetDataFrame[f'{eachAssetName}_mid_price'] = round((eachAssetDataFrame[f'{eachAssetName}_bid_price'] + eachAssetDataFrame[f'{eachAssetName}_ask_price'])/2, 5)

    ######################### RETURNS #########################

    ######################### REPRESENTATIONS #########################

    def _generateTickBars(self, endDate):

        tickBars = {}
        homeStr = os.path.expandvars('${HOME}')
        # Loop for all the assets:
        for eachAssetName in self.PORTFOLIO._portfolioDict:

            # Tick Bars
            # The timestamp doesn't need to be as index > if it is as index gives error.
            READ_PATH = f'{homeStr}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Data/{eachAssetName}_BID_ASK_{endDate}.csv'
            bars = standard_data_structures.get_tick_bars(READ_PATH, threshold=5500, batch_size=1000000, verbose=False)
            # Add them to the dict:
            tickBars[eachAssetName] = bars

    def _generateDollarBars(self, endDate):

        dollarBars = {}
        homeStr = os.path.expandvars('${HOME}')
        # Loop for all the assets:
        for eachAssetName in self.PORTFOLIO._portfolioDict:

            # Dollar Bars
            # The timestamp doesn't need to be as index > if it is as index gives error.
            READ_PATH = f'{homeStr}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Data/{eachAssetName}_BID_ASK_{endDate}.csv'
            bars = standard_data_structures.get_dollar_bars(READ_PATH, threshold=70000000, batch_size=1000000, verbose=True)
            # Add them to the dict:
            dollarBars[eachAssetName] = bars

    def getEMADollarImbalanceBars(self, endDate):

        dollarBars = {}
        homeStr = os.path.expandvars('${HOME}')
        # Loop for all the assets:
        for eachAssetName in self.PORTFOLIO._portfolioDict:

            # Dollar Bars
            # The timestamp doesn't need to be as index > if it is as index gives error.
            READ_PATH = f'{homeStr}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Data/{eachAssetName}_BID_ASK_{endDate}.csv'
            bars = standard_data_structures.get_dollar_bars(READ_PATH, threshold=70000000, batch_size=1000000, verbose=True)
            # Add them to the dict:
            dollarBars[eachAssetName] = bars

    def getEMAVolumeImbalanceBars(self, endDate):

        dollarBars = {}
        homeStr = os.path.expandvars('${HOME}')
        # Loop for all the assets:
        for eachAssetName in self.PORTFOLIO._portfolioDict:

            # Dollar Bars
            # The timestamp doesn't need to be as index > if it is as index gives error.
            READ_PATH = f'{homeStr}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Data/{eachAssetName}_BID_ASK_{endDate}.csv'
            bars = standard_data_structures.get_dollar_bars(READ_PATH, threshold=70000000, batch_size=1000000, verbose=True)
            # Add them to the dict:
            dollarBars[eachAssetName] = bars

    def getEMATickImbalanceBars(self, endDate):

        dollarBars = {}
        homeStr = os.path.expandvars('${HOME}')
        # Loop for all the assets:
        for eachAssetName in self.PORTFOLIO._portfolioDict:

            # Dollar Bars
            # The timestamp doesn't need to be as index > if it is as index gives error.
            READ_PATH = f'{homeStr}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Data/{eachAssetName}_BID_ASK_{endDate}.csv'
            bars = standard_data_structures.get_dollar_bars(READ_PATH, threshold=70000000, batch_size=1000000, verbose=True)
            # Add them to the dict:
            dollarBars[eachAssetName] = bars 

    ######################### REPRESENTATIONS #########################

    ######################### PLOTS #########################

    def _plotReturns(self, saveDirectory='', showIt=False):

        # Generates returns based on some metric.
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            print(f'[{self._plotReturns.__name__}] - Looping for asset <{eachAssetName}>...')

            # Plot the returns:
            f1, ax = plt.subplots(figsize = (10,5))
            f1.canvas.set_window_title('Returns Plot')
            plt.plot(eachAssetDataFrame.Returns.values, label='Returns')
            plt.grid(linestyle='dotted')
            plt.xlabel('Observations')
            plt.ylabel('Returns')
            plt.title(f'Asset: {eachAssetName} -- Returns Plot (First difference)')
            plt.legend(loc='best')
            plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

            # In PNG:
            plt.savefig(saveDirectory + f'/returnsPlot_{eachAssetName}.png')

            # Show it:
            if showIt: 
                plt.show()

    def _plotDistribution(self, saveDirectory='', showIt=False):

        # Generates returns based on some metric.
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            print(f'[{self._plotDistribution.__name__}] - Looping for asset <{eachAssetName}>...')

            # Plot the distribution and KDE:
            f1, ax = plt.subplots(figsize = (10,5))
            f1.canvas.set_window_title('Distribution Plot')
            sns.distplot(eachAssetDataFrame.Returns.values, color="dodgerblue", label=f'Return Distribution', fit=norm, 
                    hist_kws={"rwidth":0.90,'edgecolor':'white', 'alpha':1.0},
                    fit_kws={"color":"coral", 'linewidth':2.5, 'label':'Fit (Normal) Line'},
                    kde_kws={"color":"limegreen", 'linewidth':2.5, 'label':'KDE Line'})
            sns.distplot(eachAssetDataFrame.Returns.values, color="dodgerblue", fit=laplace, 
                    hist_kws={"rwidth":0.90,'edgecolor':'white', 'alpha':1.0},
                    fit_kws={"color":"gold", 'linestyle':'solid', 'linewidth':2.5, 'label':'Fit (Laplace) Line'})
            sns.distplot(eachAssetDataFrame.Returns.values, color="dodgerblue", fit=johnsonsu, 
                    hist_kws={"rwidth":0.90,'edgecolor':'white', 'alpha':1.0},
                    fit_kws={"color":"darkviolet", 'linestyle':'solid', 'linewidth':2.5, 'label':'Fit (Johnson) Line'})

            # Add more than one distplot will add several KDE lines to see the different distributions.
            plt.grid(linestyle='dotted')
            plt.xlabel(f'Returns Values', horizontalalignment='center', verticalalignment='center', fontsize=14, labelpad=20)
            plt.title(f'Asset: {eachAssetName} -- Distribution Returns and KDE Plot')
            plt.legend(loc='best')
            plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

            # In PNG:
            plt.savefig(saveDirectory + f'/distributionPlot_{eachAssetName}.png')

            # Show it:
            if showIt:
                plt.show()

if __name__ == "__main__":
    
    # Create some variables:
    homeStr = os.path.expanduser("~")
    plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Plots')
    dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Data')

    # Create some assets:
    assetsList = [#Asset('WS30', 'traditional', 'historical'), # Index US
                  #Asset('XAUUSD', 'traditional', 'historical'), # CryptoCurrency
                  #Asset('GDAXIm', 'traditional', 'historical'), # Index EUR
                  Asset('EURUSD', 'traditional', 'historical'), # Major
                  Asset('GBPJPY', 'traditional', 'historical')] # Minor

    # Create the research study object:
    # NOTE: If the FTP server gets stuck, just comment some assets and make it with less.
    # Or get it with tick or another offset string:
    R_STUDY = ResearchStudy(assetsList, formOrRead='form', sampleFormat='tick')
    #R_STUDY = ResearchStudy(assetsList, formOrRead='form', sampleFormat='5T')

    # Or read it from file:
    #R_STUDY = ResearchStudy(assetsList, formOrRead='read', dateHourString='2020-02-04_23')
    
    # Print the dict:
    #pprint.pprint(R_STUDY.PORTFOLIO._portfolioDict)
    #pprint.pprint(R_STUDY.PORTFOLIO._portfolioDict['WS30'])
    #pprint.pprint(R_STUDY.PORTFOLIO._portfolioDict['WS30'].shape)

    # Apply the reseach study we want:
    #R_STUDY._generateRawReturns()
    #R_STUDY._generateLogReturns()

    #R_STUDY._plotReturns(plotsSaveDirectory)
    #R_STUDY._plotDistribution(plotsSaveDirectory)

    #pprint.pprint(R_STUDY.PORTFOLIO._portfolioDict)
    