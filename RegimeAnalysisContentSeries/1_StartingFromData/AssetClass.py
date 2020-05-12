# Import darwinexapis classes:
from darwinexapis.API.TickDataAPI.DWX_TickData_Downloader_API import DWX_TickData_Downloader_API
from darwinexapis.API.TickDataAPI.DWX_TickData_Reader_API import DWX_TickData_Reader_API
from darwinexapis.API.DarwinDataAnalyticsAPI.DWX_Data_Analytics_API import DWX_Darwin_Data_Analytics_API

# Import utils:
import os, glob
import pandas as pd

class Asset(object):

    '''
    An asset is any sequence of observations that is timestamped, 
    have several values like price and volume and can be bought or sold.

    - An asset has a name, a type, data_type and values.
    - An asset type can be: traditional asset or DARWIN asset.
    - An asset data type can be historical or live data.
    - We can execute trading actions on them: buy, sell or hold.
    - Raw data conversions of assets: aggregations, differences and other transformations, 
        in subsequent levels (representations to features to signals).
    '''

    def __init__(self, assetName, assetType, assetDataType):

        # Create the attributes:
        self.assetName = assetName
        self.assetType = assetType
        self.assetDataType = assetDataType

        # Create the path you wish to save the data:                                         
        self.SAVE_PATH = os.path.expandvars('${HOME}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Data/')

        # Create the ftp credentials:
        if assetType == 'traditional':

            # Create the downloader object:
            from FTP_TraditionalAssets import FTP_CREDENTIALS
            self.DOWNLOADER = DWX_TickData_Downloader_API(dwx_ftp_user=FTP_CREDENTIALS['username'], 
                                                     dwx_ftp_pass=FTP_CREDENTIALS['password'],
                                                     dwx_ftp_hostname=FTP_CREDENTIALS['server'],
                                                     dwx_ftp_port=FTP_CREDENTIALS['port'])

        elif assetType == 'darwin':

            # Create the downloader object:
            from FTP_DarwinAssets import FTP_CREDENTIALS
            self.DOWNLOADER = DWX_Darwin_Data_Analytics_API(dwx_ftp_user=FTP_CREDENTIALS['username'], 
                                                            dwx_ftp_pass=FTP_CREDENTIALS['password'],
                                                            dwx_ftp_hostname=FTP_CREDENTIALS['server'],
                                                            dwx_ftp_port=FTP_CREDENTIALS['port'])

        # Based on the requested data, execute:
        if assetDataType == 'historical':

            if assetType == 'traditional':

                # Create the DF and the dates:
                self._dataDF = None
                self.startDate, self.endDate = '2020-02-03', '2020-02-05'

                # Assign the method to a more general one:
                self._getData = self._getHistoricalDataOfTraditionalAsset

            elif assetType == 'darwin':

                # Create the DF and the dates:
                self._dataDF = None
                self.startDate, self.endDate = '2019-01-01', '2019-03-03'

                # Assign the method to a more general one:
                self._getData = self._getHistoricalDataOfDarwinAsset

        # Will request live data if we want to make a Strategy or Model out of it:
        elif assetDataType == 'live':
            pass

    ########################### TRADITIONAL ASSET DATA ###########################

    def _getHistoricalDataOfTraditionalAsset(self, sampleFormat):

        # Get the data:
        BID_DATE_DATA = self.DOWNLOADER._download_month_data_bid(_asset=self.assetName, 
                                                                 _start_date=self.startDate, 
                                                                 _end_date=self.endDate, 
                                                                 _verbose=True)
        
        # Save the data:
        self.DOWNLOADER._save_df_to_pickle(BID_DATE_DATA, which_path=self.SAVE_PATH)

        # Get the data:                                    
        ASK_DATE_DATA = self.DOWNLOADER._download_month_data_ask(_asset=self.assetName, 
                                                                 _start_date=self.startDate, 
                                                                 _end_date=self.endDate, 
                                                                 _verbose=True)

        # Save the data:
        self.DOWNLOADER._save_df_to_pickle(ASK_DATE_DATA, which_path=self.SAVE_PATH)

        # Join the two data structures:
        self._dataDF = self._joinBidAndAskHistoricalData(self.assetName, sampleFormat)

    def _joinBidAndAskHistoricalData(self, assetName, sampleFormat):

        # NOTE: CHANGE THE PATHS DEPENDING ON THE DOWNLOADED DATA!
        homeStr = os.path.expandvars('${HOME}')
        bidData = glob.glob(f'{homeStr}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Data/{assetName}_BID_*.pkl')[0]
        askData = glob.glob(f'{homeStr}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Data/{assetName}_ASK_*.pkl')[0]

        # Generate the object: 
        READER = DWX_TickData_Reader_API(_bids_file=bidData, 
                                         _asks_file=askData)

        # Generate the dataframe: 
        combinedDataFrame = READER._get_symbol_as_dataframe_(_convert_epochs=True,
                                                            _check_integrity=False,
                                                            _calc_spread=True,
                                                            _reindex=[],
                                                            _precision=sampleFormat)
        
        # Save it:                                                                                           
        READER._save_df_to_csv(combinedDataFrame, which_path=self.SAVE_PATH)

        # Return it:
        return combinedDataFrame

    def _readBidAndAskHistoricalData(self, assetName, endDate):

        # Read the data from the .csv file:
        homeStr = os.path.expandvars('${HOME}')
        READ_PATH = f'{homeStr}/Desktop/AlphaTeamDX/RegimeAnalysisContentSeries/Data/{assetName}_BID_ASK_{endDate}.csv'

        # Load in df:
        self._dataDF = pd.read_csv(READ_PATH, index_col=0)

    ########################### TRADITIONAL ASSET DATA ###########################

    ########################### DARWIN ASSET DATA ###########################

    def _getHistoricalDataOfDarwinAsset(self, assetSuffix):

        # Get the data:
        quotes = self.DOWNLOADER.get_quotes_from_ftp(darwin=self.assetName,
                                                     suffix=assetSuffix,
                                                     monthly=True, # If set to False, month/year used > If True ALL data available
                                                     month=self.startDate,
                                                     year=self.endDate)

    ########################### DARWIN ASSET DATA ###########################

if __name__ == "__main__":
    
    ASSET = Asset('WS30', 'traditional', 'historical')
    ASSET._getData('tick')
    print(ASSET._dataDF.head())

    #ASSET_2 = Asset('WS30', 'traditional', 'historical')
    #ASSET_2._readBidAndAskHistoricalData('WS30', '2018-01-04_23')
    #print(ASSET_2._dataDF.head())