# Imports:
from PortfolioClass import Portfolio
from ModelClass import Model
from darwinexapis.API.InvestorAccountInfoAPI.DWX_AccInfo_API import DWX_AccInfo_API
from darwinexapis.API.TradingAPI.DWX_Trading_API import DWX_Trading_API

# Import utils:
import os, glob
import pandas as pd

class Strategy(Model, Portfolio):

    '''
    Actionable decisions on a Portfolio object.
    
    - An Strategy will make Buy, Sell and Hold actions on a Portfolio object.
    - An Strategy will make use of InvestorAcc + tradingAPI.
    - An Strategy is the general view on everything that is needed (schedules, timezones, actions...).
    '''

    def __init__(self):

        pass