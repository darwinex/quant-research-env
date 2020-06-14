### First, we append the previous level to the sys.path var:
import sys, os
### We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Imports:
from RegimeAnalysisContentSeries.Python_Classes.PortfolioClass import Portfolio
from RegimeAnalysisContentSeries.Python_Classes.ResearchStudyClass import ResearchStudy

# Import utils:
import glob
import pandas as pd

class BaseModel(ResearchStudy):

    '''A Model will hold the data entry for the portfolio + create the decision making that strategy will use.

    - A Model will get some input data (i.e. X, attributes, random variables).
    - A Model will need to define its parameters.
    - A Model will need to be fitted to the data.
    - A Model will need to output a result after performing the previous steps.
    '''

    def __init__(self, name, assetsList, formOrRead='read_features', dateHourString=''):

        # Initialize the ResearchStudy class:
        super().__init__(assetsList, formOrRead, dateHourString)

        # Create the name of the model:
        self.name = name

    def _defineModelParameters(self):

        pass

    def _inputVariables(self, inputVars):

        pass
    
    def _outputVariable(self):

        pass

    def _fitTheModel(self):

        pass

    def _saveModel(self):

        pass    