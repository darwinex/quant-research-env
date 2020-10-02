# First, we append the previous level to the sys.path var:
import sys, os, pandas as pd
# We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Import the base model:
from RegimeAnalysisContentSeries.Python_Classes.FTP_DarwinAssets import FTP_CREDENTIALS

### Import the different classes:
from darwinexapis.API.DarwinDataAnalyticsAPI.DWX_Data_Analytics_API import DWX_Darwin_Data_Analytics_API
from darwinexapis.API.InfoAPI.DWX_Info_API import DWX_Info_API
from darwinexapis.API.InvestorAccountInfoAPI.DWX_AccInfo_API import DWX_AccInfo_API
from darwinexapis.API.QuotesAPI.DWX_Quotes_API import DWX_Quotes_API
from darwinexapis.API.TradingAPI.DWX_Trading_API import DWX_Trading_API
from darwinexapis.API.WebSocketAPI.DWX_WebSocket_API import DWX_WebSocket_API

class CharlesDarwinClass(object):

    def __init__(self,):

        ### Let's create the auth credentials:
        self.AUTH_CREDS = {'access_token': 'YOUR_ALPHA_TOKEN',
                           'consumer_key': 'YOUR_ALPHA_TOKEN',
                           'consumer_secret': 'YOUR_ALPHA_TOKEN',
                           'refresh_token': 'YOUR_ALPHA_TOKEN'}
        
        # Get the FTP downloader:
        self.HISTORICAL_API = DWX_Darwin_Data_Analytics_API(dwx_ftp_user=FTP_CREDENTIALS['username'], 
                                                            dwx_ftp_pass=FTP_CREDENTIALS['password'],
                                                            dwx_ftp_hostname=FTP_CREDENTIALS['server'],
                                                            dwx_ftp_port=FTP_CREDENTIALS['port'])
    
    ######################################## Analysis API ########################################

    def _getDARWINHistoricalData(self, darwin, riskSuffix, allData, month, year, formerOrNew, saveTheData):

        # Get quote date for DARWINs:
        # This call will get all the data and will take some time to execute.
        quotes = self.HISTORICAL_API.get_quotes_from_ftp(darwin=darwin,
                                                            suffix=riskSuffix,
                                                            monthly=allData, # If set to False, month/year used > If True ALL data available
                                                            month=month,
                                                            year=year, 
                                                            former_or_new=formerOrNew)
        if saveTheData:
            self.HISTORICAL_API.save_data_to_csv(quotes, which_path=os.path.expandvars('${HOME}/Desktop/'), filename=f'{darwin}_{formerOrNew}_Quotes')

        # Print it:
        #print(quotes.head())
        #print(quotes.shape)
        return quotes

    def _loadDARWINHistoricalData(self, loadDirectory):

        # Load the csv:
        DARWIN_QUOTE_DATA = pd.read_csv(loadDirectory, index_col=0, parse_dates=True, infer_datetime_format=True)

        # Return it:
        return DARWIN_QUOTE_DATA

if __name__ == "__main__":

    # Get it:
    CHARLES = CharlesDarwinClass()

    CHARLES._getDARWINHistoricalData(darwin='SYO', 
                                     riskSuffix='4.24', 
                                     allData=True, 
                                     month='05', 
                                     year='2018',
                                     formerOrNew='former',
                                     saveTheData=True)