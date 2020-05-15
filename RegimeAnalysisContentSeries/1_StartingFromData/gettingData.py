# Import the class:
from ResearchStudyClass import ResearchStudy
from AssetClass import Asset
import os, pprint

# Create some path variables > Point them to the specific folder:
homeStr = os.path.expanduser("~")
plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Plots')
dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Data/Data_DF')

# Create some assets:
assetsList = [Asset('WS30', 'traditional', 'historical'), # Index US
              Asset('XAUUSD', 'traditional', 'historical'), # CryptoCurrency
              Asset('GDAXIm', 'traditional', 'historical'), # Index EUR
              Asset('EURUSD', 'traditional', 'historical'), # Major
              Asset('GBPJPY', 'traditional', 'historical')] # Minor

# Create the research study object:
# Get the tick data or some time aggregated representation: 
#R_STUDY = ResearchStudy(assetsList, formOrRead='form', sampleFormat='tick')
#R_STUDY = ResearchStudy(assetsList, formOrRead='form', sampleFormat='5T')

# Or read it from file:
# NOTE: If the data is not in the /Data directory> 
# we will need to change the path in the AssetClass _readBidAndAskHistoricalData method.
R_STUDY = ResearchStudy(assetsList, formOrRead='read', dateHourString='2020-02-04_23')

# Let's see the data:
pprint.pprint(R_STUDY.PORTFOLIO._portfolioDict['WS30'])

# Perform some calculations on the data:
R_STUDY._generateRawReturns()

# Save the generated dataframes:
R_STUDY._saveGeneratedDataFrames(dataframesSaveDirectory)