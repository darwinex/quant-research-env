### First, we append the previous level to the sys.path var:
import sys, os
### We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Import the base model:
from RegimeAnalysisContentSeries.Python_Classes.AssetClass import Asset
from RegimeAnalysisContentSeries.Python_Classes.ResearchStudyClass import ResearchStudy
from RegimeAnalysisContentSeries.Python_Classes.ModelClass import BaseModel

# Import some utils:
import numpy as np, pandas as pd
import talib as tb

# Import Kalman Filter package:
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise, Saver

### Import plotting things:
import matplotlib.pyplot as plt
from matplotlib import style, cm
import matplotlib.dates as mdates
style.use('dark_background')

# Import utils:
import logging, pickle
logger = logging.getLogger()

class KalmanFilterCloseModel(BaseModel):

    def __init__(self):

        # Create some assets:
        assetsList = [Asset('WS30', 'traditional', 'historical'), # Index US
                      Asset('XAUUSD', 'traditional', 'historical'), # Commodity
                      Asset('GDAXIm', 'traditional', 'historical'), # Index EUR
                      Asset('EURUSD', 'traditional', 'historical'), # Major
                      Asset('GBPJPY', 'traditional', 'historical')] # Minor

        # Initialize the ResearchStudy class:
        super().__init__('KalmanFilterCloseModel', assetsList)

        # Make a random seed to reproduce results:
        np.random.seed(33)

        # Print to see if working:
        logger.warning(self.PORTFOLIO._portfolioDict['WS30'])

    def _defineModelParameters(self):

        '''1) It is very important to set the intial values correctly; the KF will rapidly move onto the real ones, but maybe we don't see them in the plots
        because of that.
        2) The transition covariance is also very important. Depending on that value, the transition between states will allow to have more variance or less.
        We see that in the returns plot. If we don't increase that value, we see that we don't exactly approximate the quantities of returns. If we increase it, it will approximate more.'''

        # Use the normal Kalman Filter
        self.kalmanFilter = KalmanFilter(dim_x=1, dim_z=1)

        # We will specify the parameters like the covariance matrices by hand.
        self.kalmanFilter.x = np.array([0.0], dtype=float)
        logger.warning('###########################################')
        logger.warning(f'X: {self.kalmanFilter.x}')
        logger.warning(f'X shape: {self.kalmanFilter.x.shape}')
        logger.warning('###########################################')

        self.kalmanFilter.P = np.array([[1.0]], dtype=float)
        logger.warning(f'P: {self.kalmanFilter.P}')
        logger.warning(f'P shape: {self.kalmanFilter.P.shape}')
        logger.warning('###########################################')

        self.kalmanFilter.R = np.array([[0.001]], dtype=float)
        logger.warning(f'R: {self.kalmanFilter.R}')
        logger.warning(f'R shape: {self.kalmanFilter.R.shape}')
        logger.warning('###########################################')
                
        self.kalmanFilter.F = np.array([[1.0]], dtype=float)
        logger.warning(f'F: {self.kalmanFilter.F}')
        logger.warning(f'F shape: {self.kalmanFilter.F.shape}')
        logger.warning('###########################################')

        self.kalmanFilter.H = np.array([[1.0]], dtype=float)
        logger.warning(f'H: {self.kalmanFilter.H}')
        logger.warning(f'H shape: {self.kalmanFilter.H.shape}')
        logger.warning('###########################################')

        self.kalmanFilter.Q = np.array([[1.e-05]], dtype=float)
        logger.warning(f'Q: {self.kalmanFilter.Q}')
        logger.warning(f'Q shape: {self.kalmanFilter.Q.shape}')
        logger.warning('###########################################')

    def _fitTheModel(self, saveDirectory):

        '''Apply the Kalman Filter to estimate the hidden state at time t for t = [0...ntimesteps-1] given observations up to and including time t'''

        # Initialize the parameters:
        self._defineModelParameters()

        # Create Saver object
        self.saverObject = Saver(self.kalmanFilter)

        # Loop the portfolio dict:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            # Create a container for the looping:
            self.means = []

            # Re-initialize the parameters:
            self._defineModelParameters()

            # Loop each dataframe row:
            for eachIndex, eachRow in eachAssetDataFrame.iterrows():

                # Just perform the standard predict/update loop
                self.kalmanFilter.predict()
                self.kalmanFilter.update(eachRow['close'])

                # Append to list:
                self.means.append(self.kalmanFilter.x[0])
            
            # Create the new column in the dataframe: 
            eachAssetDataFrame['KFValue'] = self.means

            # NOTE: Create the slope of the KF:
            eachAssetDataFrame['KFValue_Slope'] = eachAssetDataFrame['KFValue'].pct_change()
            eachAssetDataFrame['KFValue_Binary'] = (eachAssetDataFrame['KFValue_Slope'] > 0).astype(int)
            eachAssetDataFrame['KFValue_PlotCol'] = eachAssetDataFrame['KFValue']
            #print(eachAssetDataFrame['KFValue_Slope'].head())
            #print(eachAssetDataFrame['KFValue_Binary'].head())

            # NOTE: Create a moving average to see the difference:
            # SMA
            eachAssetDataFrame['MA'] = eachAssetDataFrame['close'].rolling(window=25).mean()
            # WMA
            #eachAssetDataFrame['MA'] = tb.WMA(eachAssetDataFrame['close'].values, timeperiod=23)
            # EMA
            #eachAssetDataFrame['MA'] = tb.EMA(eachAssetDataFrame['close'].values, timeperiod=23)
            eachAssetDataFrame.dropna(how='any', inplace=True)

            # Save the filter values for further reference:
            self._saveModel(eachAssetName, saveDirectory)  

        # Print:
        logger.warning(self.PORTFOLIO._portfolioDict['WS30'])

    def _saveModel(self, eachAssetName, saveDirectory):

        # Save parameters in memory and to file:
        self.saverObject.save()

        with open(saveDirectory + f'/KFCloseParams_{eachAssetName}.pickle', 'wb') as file_path:
            pickle.dump(dict(self.saverObject._DL), file_path)

    def _plotModelOutput(self, saveDirectory='', showIt=False):

        # Plot:
        # Create the colormap:
        colormap = cm.get_cmap('cool')

        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            logger.warning(f'[{self._plotModelOutput.__name__}] - Looping for asset <{eachAssetName}>...')

            # We will just get part of the dataframe for the plot:
            eachAssetDataFrame_Little = eachAssetDataFrame[:100].copy()
            eachAssetDataFrame_Little['date'] =  range(1, len(eachAssetDataFrame_Little) + 1)
            logger.warning(eachAssetDataFrame_Little.head())

            # Create the figure:
            f1, ax = plt.subplots(figsize = (10,5))

            # Create the plots:
            ax.plot(eachAssetDataFrame_Little.date, eachAssetDataFrame_Little.close, label='Close')
            ax.plot(eachAssetDataFrame_Little.date, eachAssetDataFrame_Little.KFValue, label='KFValue')
            ax.plot(eachAssetDataFrame_Little.date, eachAssetDataFrame_Little.MA, label='SMA')
            ax.scatter(eachAssetDataFrame_Little.date, eachAssetDataFrame_Little.KFValue_PlotCol, 
                       #c=eachAssetDataFrame_Little.KFValue_Slope,
                       c=eachAssetDataFrame_Little.KFValue_Binary,
                       cmap=colormap,
                       label='KF Slope',
                       s=80)
            ax.grid(True)

            plt.grid(linestyle='dotted')
            plt.xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=14, labelpad=20)
            plt.ylabel('Values', horizontalalignment='center', verticalalignment='center', fontsize=14, labelpad=20)
            ax.legend(loc='best')
            plt.title(f'Close and Kalman Filter value for asset <{eachAssetName}>')
            plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
            f1.canvas.set_window_title('Kalman Filtering Plot')

            # In PNG:
            plt.savefig(saveDirectory + f'/KFClose_{eachAssetName}.png')

            # Show it:
            if showIt: 
                plt.show()

if __name__ == "__main__":
    
    # Generate the paths:
    homeStr = os.path.expanduser("~")
    plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Plots/Plots_KF')
    dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Data/Data_Others')
    featuresReadingDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Data/Data_Others')
    modelSavingDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Models')

    # Execute:
    KF = KalmanFilterCloseModel()
    KF._fitTheModel(modelSavingDirectory)
    KF._plotModelOutput(plotsSaveDirectory, showIt=True)