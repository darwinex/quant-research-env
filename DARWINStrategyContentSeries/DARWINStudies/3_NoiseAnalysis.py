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

# Apply the reseach study we want:
R_STUDY._generateResampledAndFilteredSeries(resampleRule='4H')

# Print it:
pprint.pprint(R_STUDY.PORTFOLIO._portfolioDict)

# Save the generated dataframes:
R_STUDY._saveDarwinGeneratedDataFrames(dataframesSaveDirectory)