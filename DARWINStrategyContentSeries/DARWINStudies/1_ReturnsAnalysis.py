### First, we append the previous level to the sys.path var:
import sys, os
### We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Import the class:
from RegimeAnalysisContentSeries.Python_Classes.AssetClass import Asset
from RegimeAnalysisContentSeries.Python_Classes.ResearchStudyClass import ResearchStudy
import os, pprint

# Create some assets:
assetsList = [Asset('PLF_4.1', 'darwin', 'historical'),
              Asset('LVS_4.20', 'darwin', 'historical'),
              Asset('SYO_4.24', 'darwin', 'historical')]

# Create some path variables > Point them to the specific folder:
homeStr = os.path.expanduser("~")
plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/DARWINStrategyContentSeries/Data')
dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/DARWINStrategyContentSeries/Data')

#R_STUDY = ResearchStudy(assetsList, formOrRead='form_darwin', saveTheData=True)
R_STUDY = ResearchStudy(assetsList, formOrRead='read_darwin', formerOrNew='former')

# Print it:
pprint.pprint(R_STUDY.PORTFOLIO._portfolioDict)

###################### DARWIN SPECIFICS ######################
# Apply the reseach study we want:
R_STUDY._generateResampledAndFilteredSeries(resampleRule='1D')
#R_STUDY._generateResampledAndFilteredSeries(resampleRule='4H')
#R_STUDY._generateResampledAndFilteredSeries(resampleRule='30min')
###################### DARWIN SPECIFICS ######################

# Apply the reseach study we want:
#R_STUDY._generateRawReturns()
R_STUDY._generateLogReturns()
#R_STUDY._generateRollingMean(rollingWindow=40)

# Plot candles and indicators:
R_STUDY._plotCandleAndIndicators(plotsSaveDirectory, showIt=True)
#R_STUDY._plotCandleAndIndicatorsNEW(plotsSaveDirectory, showIt=True)

# Generate the plots:
R_STUDY._plotReturns(plotsSaveDirectory, showIt=True)
#R_STUDY._plotLine(plotsSaveDirectory, showIt=True)
#R_STUDY._plotReturns(plotsSaveDirectory, showIt=True, rollingMeanOrNot=True)
R_STUDY._plotDistribution(plotsSaveDirectory, showIt=True)
#R_STUDY._plotQQPlot(plotsSaveDirectory, showIt=True)

# Save the generated dataframes:
R_STUDY._saveDarwinGeneratedDataFrames(dataframesSaveDirectory)