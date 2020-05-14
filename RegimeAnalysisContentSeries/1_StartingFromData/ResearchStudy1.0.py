# Import the class:
from ResearchStudyClass import ResearchStudy
from AssetClass import Asset
import os

# Create some path variables > Point them to the specific folder:
homeStr = os.path.expanduser("~")
plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Plots')
dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Data')

# Create some assets:
assetsList = [Asset('WS30', 'traditional', 'historical'), # Index US
                  Asset('XAUUSD', 'traditional', 'historical'), # CryptoCurrency
                  Asset('GDAXIm', 'traditional', 'historical'), # Index EUR
                  Asset('EURUSD', 'traditional', 'historical'), # Major
                  Asset('GBPJPY', 'traditional', 'historical')] # Minor

# Create the research study object:
# NOTE: If the FTP server gets stuck, just comment some assets and make it with less.
# Get the tick data or some time aggregated representation: 
#R_STUDY = ResearchStudy(assetsList, formOrRead='form', sampleFormat='tick')
#R_STUDY = ResearchStudy(assetsList, formOrRead='form', sampleFormat='5T')

# Or read it from file:
# NOTE: If the data is not in the /Data directory> 
# we will need to change the path in the AssetClass _readBidAndAskHistoricalData method.
R_STUDY = ResearchStudy(assetsList, formOrRead='read', dateHourString='2020-02-04_23')
    
# Print the whole dict, some asset or the shape:
#pprint.plogger.warning(R_STUDY.PORTFOLIO._portfolioDict)
#pprint.plogger.warning(R_STUDY.PORTFOLIO._portfolioDict['WS30'])
#pprint.plogger.warning(R_STUDY.PORTFOLIO._portfolioDict['WS30'].shape)

# Apply the reseach study we want:
#R_STUDY._generateRawReturns()
R_STUDY._generateLogReturns()
R_STUDY._generateRollingMean()

# Generate the plots:
R_STUDY._plotReturns(plotsSaveDirectory, showIt=True)
R_STUDY._plotDistribution(plotsSaveDirectory, showIt=True)