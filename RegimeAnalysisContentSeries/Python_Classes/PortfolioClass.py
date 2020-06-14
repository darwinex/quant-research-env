### First, we append the previous level to the sys.path var:
import sys, os
### We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Imports:
from RegimeAnalysisContentSeries.Python_Classes.AssetClass import Asset

# Import utils:
import glob, pprint
import pandas as pd

class Portfolio(Asset):

    '''
    A portfolio is an object composed of X number of Assets. It inherits
    the functionality of the Asset class and its characteristics.

    - A portfolio can be composed of 1 or more assets of the same or different type.
    - A portfolio object has a n_components of assets > those form a unique data structure.
    '''

    def __init__(self, portfolioAssetComponents):

        # Create the portfolio dictionary:
        self.portfolioAssetComponents = portfolioAssetComponents
        self._portfolioDict = {}

    ################### PORTFOLIO HISTORICAL DATA ###################

    def _formPortfolioHistoricalData(self, sampleFormat):
        
        # Loop and get the data:
        for eachAsset in self.portfolioAssetComponents:

            # Instantiate the object and call the method:
            eachAssetObject = eachAsset
            eachAssetObject._getData(sampleFormat)
            
            # Quit the FTP connection for cleaning:
            #eachAssetObject.DOWNLOADER._ftpObj.quit()
            self._portfolioDict[eachAssetObject.assetName] = eachAssetObject._dataDF

        # Print the dict:
        pprint.pprint(self._portfolioDict)

    def _readPortfolioHistoricalData(self, endDate):

        # Loop and get the data:
        for eachAsset in self.portfolioAssetComponents:

            # Instantiate the object and call the method:
            eachAssetObject = eachAsset

            # Read it and add it to the dictionary:
            eachAssetObject._readBidAndAskHistoricalData(eachAssetObject.assetName, endDate)
            self._portfolioDict[eachAssetObject.assetName] = eachAssetObject._dataDF

    def _readPortfolioFeaturesCsvs(self):

        # Loop and get the data:
        for eachAsset in self.portfolioAssetComponents:

            # Instantiate the object and call the method:
            eachAssetObject = eachAsset
            print(f'[_readPortfolioFeaturesCsvs] - Looping for asset {eachAssetObject.assetName}...')

            # Read it and add it to the dictionary:
            eachAssetObject._readFeaturesHistoricalData(eachAssetObject.assetName)
            self._portfolioDict[eachAssetObject.assetName] = eachAssetObject._dataDF

    ################### PORTFOLIO HISTORICAL DATA ###################

    ################### PORTFOLIO LIVE DATA ###################

    def _getPortfolioLiveData(self):

        pass

    ################### PORTFOLIO LIVE DATA ###################

if __name__ == "__main__":
    
    assetsList = [Asset('WS30', 'traditional', 'historical'), # Index US
                  Asset('XAUUSD', 'traditional', 'historical'), # CryptoCurrency
                  Asset('GDAXIm', 'traditional', 'historical'), # Index EUR
                  Asset('EURUSD', 'traditional', 'historical'), # Major
                  Asset('GBPJPY', 'traditional', 'historical')] # Minor

    PORTFOLIO = Portfolio(assetsList)
    #PORTFOLIO._formPortfolioHistoricalData('tick')
    PORTFOLIO._readPortfolioHistoricalData('2020-02-04_23')
    
    # Print it:
    pprint.pprint(PORTFOLIO._portfolioDict)
    