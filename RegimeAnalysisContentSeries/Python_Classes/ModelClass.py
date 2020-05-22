# Imports:
from RegimeAnalysisContentSeries.Python_Classes.PortfolioClass import Portfolio
from RegimeAnalysisContentSeries.Python_Classes.ResearchStudyClass import ResearchStudy

# Import utils:
import os, glob
import pandas as pd

class Model(ResearchStudy, Portfolio):

    '''A Model will hold the data entry for the portfolio + create the decision making that strategy will use.'''

    def __init__(self):

        pass