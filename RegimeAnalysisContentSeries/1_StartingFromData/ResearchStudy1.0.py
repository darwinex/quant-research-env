# Import the class:
from ResearchStudyClass import ResearchStudy
from AssetClass import Asset
import os

# Create some path variables > Point them to the specific folder:
homeStr = os.path.expanduser("~")
plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Plots/Plots_Test')
dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Data')

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
    
# Print the whole dict, some asset or the shape:
#pprint.pprint.warning(R_STUDY.PORTFOLIO._portfolioDict)
#pprint.pprint.warning(R_STUDY.PORTFOLIO._portfolioDict['WS30'])
#pprint.pprint.warning(R_STUDY.PORTFOLIO._portfolioDict['WS30'].shape)

# Apply the reseach study we want:
R_STUDY._generateRawReturns()
#R_STUDY._generateLogReturns()
#R_STUDY._generateRollingMean()
R_STUDY._generateRollingMean(rollingWindow=40)

# Generate the plots:
#R_STUDY._plotReturns(plotsSaveDirectory, showIt=True)
R_STUDY._plotReturns(plotsSaveDirectory, showIt=True, rollingMeanOrNot=True)
#R_STUDY._plotDistribution(plotsSaveDirectory, showIt=True)

# Save the generated dataframes:
#R_STUDY._saveGeneratedDataFrames(dataframesSaveDirectory)