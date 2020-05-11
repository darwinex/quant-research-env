# Imports:
from AssetClass import Asset

# Import utils:
import os, glob, pprint
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

    ###############################################################

    def _formPortfolioHistoricalData(self, sampleFormat):
        
        # Loop and get the data:
        for eachAsset in self.portfolioAssetComponents:

            # Instantiate the object and call the method:
            eachAssetObject = eachAsset
            eachAssetObject._getData(sampleFormat)
            
            # Try this:
            eachAssetObject.DOWNLOADER._ftpObj.quit()
            self._portfolioDict[eachAssetObject.assetName] = eachAssetObject._dataDF

        # Print the dict:
        pprint.pprint(self._portfolioDict)

    def _formPortfolioDataFrame(self):

        # From the dict, get the df's and concat them:
        # NOTE: NOT WORKING.
        self._portfolioDF = pd.concat(self._portfolioDict.values(), axis=1, sort=False)
        print(self._portfolioDF)

    def _readPortfolioHistoricalData(self, endDate):

        # Loop and get the data:
        for eachAsset in self.portfolioAssetComponents:
            # Instantiate the object and call the method:
            eachAssetObject = eachAsset
            eachAssetObject._readBidAndAskHistoricalData(eachAssetObject.assetName, endDate)
            self._portfolioDict[eachAssetObject.assetName] = eachAssetObject._dataDF

    ###############################################################

    def _getPortfolioLiveData(self):

        pass

if __name__ == "__main__":
    
    assetsList = [Asset('WS30', 'traditional', 'historical'), # Index US
                  Asset('XAUUSD', 'traditional', 'historical'), # CryptoCurrency
                  Asset('STOXX50E', 'traditional', 'historical'), # Index EUR
                  Asset('EURUSD', 'traditional', 'historical'), # Major
                  Asset('GBPJPY', 'traditional', 'historical')] # Minor

    PORTFOLIO = Portfolio(assetsList)
    #PORTFOLIO._formPortfolioHistoricalData('tick')
    PORTFOLIO._readPortfolioHistoricalData('2018-01-02_23')
    
    # Print it:
    pprint.pprint(PORTFOLIO._portfolioDict)
    