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
        assetsList = [Asset('PLF_4.1', 'darwin', 'historical'),
                      Asset('LVS_4.20', 'darwin', 'historical'),
                      Asset('SYO_4.24', 'darwin', 'historical')]

        self.R_STUDY = ResearchStudy(assetsList, formOrRead='read_darwin', formerOrNew='former')
        self.R_STUDY._generateResampledAndFilteredSeries(resampleRule='1D')

    def executeSeasonalDecompose(self, saveDirectory):

        # Loop the portfolio dict:
        for eachAssetName, eachAssetDataFrame in self.R_STUDY.PORTFOLIO._portfolioDict.items():

            # Make the decompose:
            TS_DECOMPOSED = seasonal_decompose(eachAssetDataFrame['close'], model='aditive', period=20)
            #TS_DECOMPOSED = seasonal_decompose(eachAssetDataFrame['Returns'], model='multiplicative', period=20)
            print(f'[executeSeasonalDecompose] - Will plot decomposed series for asset {eachAssetName}')

            # Plot and show it:
            TS_DECOMPOSED.plot()
            
            # In PNG:
            plt.savefig(saveDirectory + f'/TSDec_DARWIN_{eachAssetName}.png')
            plt.show()

if __name__ == "__main__":

    # Create some path variables > Point them to the specific folder:
    homeStr = os.path.expanduser("~")
    plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/DARWINStrategyContentSeries/Data')
    dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/DARWINStrategyContentSeries/Data')

    # Execute:
    TSDEC = TSDecomposition()
    TSDEC.executeSeasonalDecompose(plotsSaveDirectory)