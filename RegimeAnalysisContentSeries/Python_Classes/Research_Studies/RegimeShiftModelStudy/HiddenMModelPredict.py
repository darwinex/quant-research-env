# First, we append the previous level to the sys.path var:
import sys, os
# We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))

# Import the base model:
from RegimeAnalysisContentSeries.Python_Classes.AssetClass import Asset
from RegimeAnalysisContentSeries.Python_Classes.ResearchStudyClass import ResearchStudy
from RegimeAnalysisContentSeries.Python_Classes.ModelClass import BaseModel

# Import some utils:
import numpy as np, pandas as pd

# Import the model package > pip install hmmlearn
from hmmlearn.hmm import GaussianHMM, GMMHMM

### Import plotting things:
import matplotlib.pyplot as plt
from matplotlib import style, cm
style.use('dark_background')

# Import utils:
import logging, pickle
logger = logging.getLogger()

class HiddenMarkovModelPredictor(BaseModel):

    def __init__(self):

        # Create some assets:
        assetsList = [Asset('WS30', 'traditional', 'historical'), # Index US
                      Asset('XAUUSD', 'traditional', 'historical'), # CryptoCurrency
                      Asset('GDAXIm', 'traditional', 'historical'), # Index EUR
                      Asset('EURUSD', 'traditional', 'historical'), # Major
                      Asset('GBPJPY', 'traditional', 'historical')] # Minor

        # Initialize the ResearchStudy class:
        super().__init__('HiddenMarkovModel', assetsList)

        # Print to see if working:
        #logger.warning(self.PORTFOLIO._portfolioDict['WS30'])

    def _loadModel(self, loadDirectory):

        # Get the models dict:
        self.modelsDict = {}

        # Loop the portfolio dict:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            # Load the model:
            with open(loadDirectory + f'/HMM_{eachAssetName}.pickle', 'rb') as pickle_file:
                self.model = pickle.load(pickle_file)

            # Index it:
            self.modelsDict[eachAssetName] = self.model

    def _predictWithModel(self):

        # Loop the portfolio dict:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            # Get the returns into a 2D array > Actually, it is (X,) > We should conver to (X,1)
            RETURNS_RESHAPED = np.column_stack([eachAssetDataFrame["Returns"]])

            # Predict the hidden states based on the returns:
            HIDDEN_STATES = self.modelsDict[eachAssetName].predict(RETURNS_RESHAPED)
            #logger.warning(HIDDEN_STATES)

            # Create the new column in the dataframe: 
            eachAssetDataFrame['HiddenStates'] = HIDDEN_STATES

    def _plotModelOutput(self, saveDirectory='', showIt=False):

        # Plot:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            logger.warning(f'[{self._plotModelOutput.__name__}] - Looping for asset <{eachAssetName}>...')

            # We will just get part of the dataframe for the plot:
            eachAssetDataFrame_Little = eachAssetDataFrame[:200].copy()
            eachAssetDataFrame_Little['date'] =  range(1, len(eachAssetDataFrame_Little) + 1)

            # Create the figure:
            f1, ax = plt.subplots(3, figsize = (10,5))
    
            # Create the colormap:
            colormap = cm.get_cmap('rainbow')

            # Create the plots:
            ax[0].scatter(eachAssetDataFrame_Little.date, eachAssetDataFrame_Little.close, 
                       c=eachAssetDataFrame_Little.HiddenStates,
                       cmap=colormap,
                       label='Hidden States',
                       s=80)
            ax[0].set_xlabel('Hidden States', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[0].set_ylabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[0].legend(loc='best')

            ax[1].plot(eachAssetDataFrame_Little.date, eachAssetDataFrame_Little.close,label='Close Price')
            ax[1].set_xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[1].set_ylabel('Close Price', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[1].legend(loc='best')

            ax[2].plot(eachAssetDataFrame_Little.date,eachAssetDataFrame_Little.Returns,label='Returns')
            ax[2].set_xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[2].set_ylabel('Returns', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[2].legend(loc='best')

            plt.grid(linestyle='dotted')
            plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
            f1.canvas.set_window_title(f'Hidden Markov Model + more data plot for asset <{eachAssetName}>')
            #f1.tight_layout()
            
            # In PNG:
            plt.savefig(saveDirectory + f'/HMM_{eachAssetName}_PREDICT.png')

            # Show it:
            if showIt: 
                plt.show()

if __name__ == "__main__":
    
    # Generate the paths:
    homeStr = os.path.expanduser("~")
    loadDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Models')
    plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Plots/Plots_HMM')

    # Execute:
    HMM = HiddenMarkovModelPredictor()
    HMM._loadModel(loadDirectory)
    HMM._predictWithModel()
    HMM._plotModelOutput(plotsSaveDirectory, showIt=True)