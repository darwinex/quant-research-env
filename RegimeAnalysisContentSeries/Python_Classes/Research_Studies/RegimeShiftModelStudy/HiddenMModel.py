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

class HiddenMarkovModel(BaseModel):

    def __init__(self):

        # Create some assets:
        assetsList = [Asset('WS30', 'traditional', 'historical'), # Index US
                      Asset('XAUUSD', 'traditional', 'historical'), # CryptoCurrency
                      Asset('GDAXIm', 'traditional', 'historical'), # Index EUR
                      Asset('EURUSD', 'traditional', 'historical'), # Major
                      Asset('GBPJPY', 'traditional', 'historical')] # Minor

        # Initialize the ResearchStudy class:
        super().__init__('HiddenMarkovModel', assetsList)

        # Make a random seed to reproduce results:
        np.random.seed(33)

        # Print to see if working:
        #logger.warning(self.PORTFOLIO._portfolioDict['WS30'])

    def _defineModelParameters(self):

        # Define the model:
        #self.model = GaussianHMM(n_components=2, 
        #                         covariance_type="full", 
        #                         n_iter=200,
        #                         verbose=True)
        self.model = GMMHMM(n_components=2, 
                                 covariance_type="full", 
                                 n_iter=20,
                                 verbose=True)

    def _monitorConvergence(self):

        # Print:
        logger.warning(f"Model Converged: {self.model.monitor_.converged}")

    def _monitorHistory(self):

        # Print:
        logger.warning(f"Model History: {self.model.monitor_.history}")

    def _fitTheModel(self, saveDirectory):

        # Loop the portfolio dict:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            # Re-initialize the parameters:
            self._defineModelParameters()

            # Fit the model:
            # Get the returns into a 2D array > Actually, it is (X,) > We should conver to (X,1)
            RETURNS_RESHAPED = np.column_stack([eachAssetDataFrame["Returns"]])
            self.model.fit(RETURNS_RESHAPED)
            logger.warning(f"Model Score for asset <{eachAssetName}>: {self.model.score(RETURNS_RESHAPED)}")

            # Check convergence and history:
            self._monitorConvergence()
            self._monitorHistory()

            # Predict the hidden states based on the returns:
            HIDDEN_STATES = self.model.predict(RETURNS_RESHAPED)
            #logger.warning(HIDDEN_STATES)

            # Save the model:
            if saveDirectory:
                self._saveModel(assetModelName=eachAssetName, saveDirectory=saveDirectory)

            # Create the new column in the dataframe: 
            eachAssetDataFrame['HiddenStates'] = HIDDEN_STATES

    def _saveDataFrames(self, saveDirectory):

        # Save each dataframe:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            logger.warning(f'[{self._saveDataFrames.__name__}] - Looping for asset <{eachAssetName}>...')
            eachAssetDataFrame.to_csv(saveDirectory + f'/{eachAssetName}_DF.csv')

    def _saveModel(self, assetModelName, saveDirectory):

        # Save the model:
        with open(saveDirectory + f'/HMM_{assetModelName}.pickle', 'wb') as pickle_file:
            pickle.dump(self.model, pickle_file)

    def _loadModel(self, assetModelName, loadDirectory):

        # Load the model:
        with open(loadDirectory + f'/HMM_{assetModelName}.pickle', 'rb') as pickle_file:
            self.model = pickle.load(pickle_file)

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
            plt.savefig(saveDirectory + f'/HMM_{eachAssetName}.png')

            # Show it:
            if showIt: 
                plt.show()

if __name__ == "__main__":
    
    # Generate the paths:
    homeStr = os.path.expanduser("~")
    plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Plots/Plots_HMM')
    dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Data/Data_HMM')
    modelSavingDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Models')

    # Execute:
    HMM = HiddenMarkovModel()
    HMM._fitTheModel(saveDirectory=modelSavingDirectory)
    HMM._saveDataFrames(saveDirectory=dataframesSaveDirectory)
    HMM._plotModelOutput(plotsSaveDirectory, showIt=True)