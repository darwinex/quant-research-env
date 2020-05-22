### First, we append the previous level to the sys.path var:
import sys, os
### We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Import the class:
from RegimeAnalysisContentSeries.Python_Classes.ResearchStudyClass import ResearchStudy
from RegimeAnalysisContentSeries.Python_Classes.AssetClass import Asset
import os

# Create some path variables > Point them to the specific folder:
homeStr = os.path.expanduser("~")
plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Plots/Plots_Others')
dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Data/Data_Others')

# Create some assets:
assetsList = [Asset('WS30', 'traditional', 'historical'), # Index US
              Asset('XAUUSD', 'traditional', 'historical'), # CryptoCurrency
              Asset('GDAXIm', 'traditional', 'historical'), # Index EUR
              Asset('EURUSD', 'traditional', 'historical'), # Major
              Asset('GBPJPY', 'traditional', 'historical')] # Minor

# Read it from file:
# NOTE: If the data is not in the /Data directory> 
# we will need to change the path in the AssetClass _readBidAndAskHistoricalData method.
R_STUDY = ResearchStudy(assetsList, formOrRead='read', dateHourString='2020-02-04_23')
    
# Apply the reseach study we want:
R_STUDY._generateTickBars(endDate='2020-02-04_23', threshold=1522)
#R_STUDY._generateDollarBars(endDate='2020-02-04_23', threshold=7000000000)

# Generate the plots:
#R_STUDY._plotReturnsOtherBars(plotsSaveDirectory, showIt=True)
R_STUDY._plotDistributionOtherBars(plotsSaveDirectory, showIt=True)
R_STUDY._plotQQPlotOtherBars(plotsSaveDirectory, showIt=True)

# Save the generated dataframes:
#R_STUDY._saveGeneratedDataFramesOtherBars(dataframesSaveDirectory)