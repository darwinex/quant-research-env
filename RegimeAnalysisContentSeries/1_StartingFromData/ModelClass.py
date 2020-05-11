# Imports:
from PortfolioClass import Portfolio
from ResearchStudyClass import ResearchStudy

# Import utils:
import os, glob
import pandas as pd

class Model(ResearchStudy, Portfolio):

    '''A Model will hold the data entry for the portfolio + create the decision making that strategy will use.'''

    def __init__(self):

        pass