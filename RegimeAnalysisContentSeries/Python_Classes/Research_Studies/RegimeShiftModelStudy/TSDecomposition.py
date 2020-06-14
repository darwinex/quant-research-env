### First, we append the previous level to the sys.path var:
import sys, os
### We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Import the base model:
from RegimeAnalysisContentSeries.Python_Classes.AssetClass import Asset
from RegimeAnalysisContentSeries.Python_Classes.ResearchStudyClass import ResearchStudy
from RegimeAnalysisContentSeries.Python_Classes.ModelClass import BaseModel

# Import some utils:
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

### Import plotting things:
import matplotlib.pyplot as plt

class TSDecomposition(BaseModel):

    def __init__(self):

        # Create some assets:
        assetsList = [Asset('WS30', 'traditional', 'historical'), # Index US
                      Asset('XAUUSD', 'traditional', 'historical'), # CryptoCurrency
                      Asset('GDAXIm', 'traditional', 'historical'), # Index EUR
                      Asset('EURUSD', 'traditional', 'historical'), # Major
                      Asset('GBPJPY', 'traditional', 'historical')] # Minor

        # Create the RSTUDY object:
        self.R_STUDY = ResearchStudy(assetsList, formOrRead='read_features')

        # Print to see if working:
        #print(self.R_STUDY.PORTFOLIO._portfolioDict['WS30'])

    def executeSeasonalDecompose(self):

        # Loop the portfolio dict:
        for eachAssetName, eachAssetDataFrame in self.R_STUDY.PORTFOLIO._portfolioDict.items():

            # Make the decompose:
            TS_DECOMPOSED = seasonal_decompose(eachAssetDataFrame['close'], model='aditive', period=20)
            #TS_DECOMPOSED = seasonal_decompose(eachAssetDataFrame['Returns'], model='multiplicative', period=20)
            print(f'')
            print(f'[executeSeasonalDecompose] - Will plot decomposed series for asset {eachAssetName}')

            # Plot and show it:
            TS_DECOMPOSED.plot()
            plt.show()

if __name__ == "__main__":
    
    # Generate the paths:
    homeStr = os.path.expanduser("~")
    plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Plots/Plots_Others')
    dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Data/Data_Others')
    featuresReadingDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Data/Data_Others')

    # Execute:
    TSDEC = TSDecomposition()
    TSDEC.executeSeasonalDecompose()