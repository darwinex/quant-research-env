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

# Import statsmodels:
import statsmodels.api as sm

### Import plotting things:
import matplotlib.pyplot as plt
from matplotlib import style, cm
style.use('dark_background')

# Import utils:
import logging, pickle
logger = logging.getLogger()

class MarkovAutoRegressiveModels(BaseModel):

    def __init__(self):

        # Create some assets:
        assetsList = [Asset('WS30', 'traditional', 'historical'), # Index US
                      Asset('XAUUSD', 'traditional', 'historical'), # Commodity
                      Asset('GDAXIm', 'traditional', 'historical'), # Index EUR
                      Asset('EURUSD', 'traditional', 'historical'), # Major
                      Asset('GBPJPY', 'traditional', 'historical') # Minor
                      ] 
        # Initialize the ResearchStudy class:
        super().__init__('MarkovAutoRegressiveModels', assetsList)

        # Print to see if working:
        #logger.warning(self.PORTFOLIO._portfolioDict['WS30'])

    def _defineModelParameters(self, whichModel, dataDF, exogVarDF):

        if whichModel == 'filardo':
            # Refs: https://www.statsmodels.org/stable/generated/statsmodels.tsa.regime_switching.markov_autoregression.MarkovAutoregression.html

            # Define the model:
            self.componentsQty = 2
            self.model = sm.tsa.MarkovAutoregression(dataDF, 
                                                     k_regimes=self.componentsQty, 
                                                     order=4, 
                                                     switching_ar=False,
                                                     #switching_ar=True,
                                                     #switching_trend=True,
                                                     #switching_variance=True,
                                                     # Time varying transition probabilities > exog_tvtp
                                                     exog_tvtp=sm.add_constant(exogVarDF))

    def _fitTheModel(self, whichModel, saveDirectory):

        '''Filtered refers to an estimate of the probability at time t based on data up to 
        and including time t (but excluding time t+1,...,T). 
        Smoothed refers to an estimate of the probability at time t using all the data in the sample'''

        # Loop the portfolio dict:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            logger.warning(f'Fitting the model for asset <{eachAssetName}>...')

            # Add column for MA:
            #eachAssetDataFrame['ReturnsSecond'] = eachAssetDataFrame['Returns'].pct_change()
            eachAssetDataFrame['MA'] = eachAssetDataFrame['close'].rolling(window=25).mean()
            eachAssetDataFrame.dropna(how='any', inplace=True)

            # Re-initialize the parameters:
            self._defineModelParameters(whichModel, eachAssetDataFrame['Returns'], eachAssetDataFrame['MA'])

            if whichModel == 'filardo':

                # Fit the model:
                np.random.seed(222)
                self.resultModel = self.model.fit(em_iter=100)
                #self.resultModel = self.model.fit()

                # Get the summary of the model:
                self._getSummaryOfModel()

                # Get the expected durations:
                self._getExpectedDurations()

                # Get probalities in pandas:
                # The final index is related to the regime.
                eachAssetDataFrame['FilteredProbs1'] = self.resultModel.filtered_marginal_probabilities[0]
                eachAssetDataFrame['SmoothedProbs1'] = self.resultModel.smoothed_marginal_probabilities[0]
                eachAssetDataFrame['FilteredProbs2'] = self.resultModel.filtered_marginal_probabilities[1]
                eachAssetDataFrame['SmoothedProbs2'] = self.resultModel.smoothed_marginal_probabilities[1]
                #eachAssetDataFrame['FilteredProbs3'] = self.resultModel.filtered_marginal_probabilities[2]
                #eachAssetDataFrame['SmoothedProbs3'] = self.resultModel.smoothed_marginal_probabilities[2]

    def _getSummaryOfModel(self):

        # Print the model summary:
        logger.warning('We will print the model summary:')
        logger.warning(self.resultModel.summary())

    def _getExpectedDurations(self):

        # Print the model expected durations of states:
        logger.warning('We will print the model expected duration of states:')
        logger.warning(self.resultModel.expected_durations)

    def _saveDataFrames(self, saveDirectory):

        # Save each dataframe:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            logger.warning(f'[{self._saveDataFrames.__name__}] - Looping for asset <{eachAssetName}>...')
            eachAssetDataFrame.to_csv(saveDirectory + f'/{eachAssetName}_MAR3_DF.csv')

    def _saveModel(self, assetModelName, saveDirectory):

        # Save the model:
        with open(saveDirectory + f'/MarkovAR3_{assetModelName}.pickle', 'wb') as pickle_file:
            pickle.dump(self.model, pickle_file)

    def _loadModel(self, assetModelName, loadDirectory):

        # Load the model:
        with open(loadDirectory + f'/MarkovAR3_{assetModelName}.pickle', 'rb') as pickle_file:
            self.model = pickle.load(pickle_file)

    def _plotModelOutputFilter(self, saveDirectory='', showIt=False):

        # Plot:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            logger.warning(f'[{self._plotModelOutputFilter.__name__}] - Looping for asset <{eachAssetName}>...')

            # We will just get part of the dataframe for the plot:
            #eachAssetDataFrame_Little = eachAssetDataFrame[:200].copy()
            eachAssetDataFrame['date'] =  range(1, len(eachAssetDataFrame) + 1)

            # Create the figure:
            f1, ax = plt.subplots(self.componentsQty + 2, figsize = (12,7))

            # Create the plots:
            ax[0].plot(eachAssetDataFrame.date, eachAssetDataFrame.FilteredProbs1,label='FProbs_Reg1')
            ax[0].set_xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[0].set_ylabel('Probabilities', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[0].legend(loc='best')

            ax[1].plot(eachAssetDataFrame.date,eachAssetDataFrame.FilteredProbs2,label='FProbs_Reg2')
            ax[1].set_xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[1].set_ylabel('Probabilities', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[1].legend(loc='best')

            ax[2].plot(eachAssetDataFrame.date,eachAssetDataFrame.Returns,label='Returns',color='gold',linewidth=2)
            ax[2].set_xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[2].set_ylabel('Returns', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[2].legend(loc='best')

            ax[3].plot(eachAssetDataFrame.date,eachAssetDataFrame.close,label='Close Price',color='gold',linewidth=2)
            ax[3].set_xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[3].set_ylabel('Close price', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[3].legend(loc='best')

            plt.grid(linestyle='dotted')
            plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
            f1.canvas.set_window_title(f'Probabilities + more data in Markov AR Hamilton plot for asset <{eachAssetName}>')
            #f1.tight_layout()

            # In PNG:
            plt.savefig(saveDirectory + f'/MarkovAR3_{eachAssetName}.png')

            # Show it:
            if showIt: 
                plt.show()

    def _plotModelOutputSmoother(self, saveDirectory='', showIt=False):

        # Plot:
        for eachAssetName, eachAssetDataFrame in self.PORTFOLIO._portfolioDict.items():

            logger.warning(f'[{self._plotModelOutputSmoother.__name__}] - Looping for asset <{eachAssetName}>...')

            # We will just get part of the dataframe for the plot:
            #eachAssetDataFrame_Little = eachAssetDataFrame[:200].copy()
            eachAssetDataFrame['date'] =  range(1, len(eachAssetDataFrame) + 1)

            # Create the figure:
            f1, ax = plt.subplots(self.componentsQty + 2, figsize = (12,7))

            # Create the plots:
            ax[0].plot(eachAssetDataFrame.date, eachAssetDataFrame.SmoothedProbs1,label='SProbs_Reg1')
            ax[0].set_xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[0].set_ylabel('Probabilities', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[0].legend(loc='best')

            ax[1].plot(eachAssetDataFrame.date,eachAssetDataFrame.SmoothedProbs2,label='SProbs_Reg2')
            ax[1].set_xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[1].set_ylabel('Probabilities', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[1].legend(loc='best')

            ax[2].plot(eachAssetDataFrame.date,eachAssetDataFrame.Returns,label='Returns',color='gold',linewidth=2)
            ax[2].set_xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[2].set_ylabel('Returns', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[2].legend(loc='best')

            ax[3].plot(eachAssetDataFrame.date,eachAssetDataFrame.close,label='Close Price',color='gold',linewidth=2)
            ax[3].set_xlabel('Observations', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[3].set_ylabel('Close price', horizontalalignment='center', verticalalignment='center', fontsize=12, labelpad=20)
            ax[3].legend(loc='best')

            plt.grid(linestyle='dotted')
            plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
            f1.canvas.set_window_title(f'Probabilities + more data in Markov AR Hamilton plot for asset <{eachAssetName}>')
            #f1.tight_layout()

            # In PNG:
            plt.savefig(saveDirectory + f'/MarkovAR3_{eachAssetName}.png')

            # Show it:
            if showIt: 
                plt.show()

if __name__ == "__main__":
    
    # Generate the paths:
    homeStr = os.path.expanduser("~")
    plotsSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Plots/Plots_MarkovAR')
    dataframesSaveDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Data/Data_MarkovAR')
    modelSavingDirectory = os.path.expandvars(f'{homeStr}/Desktop/quant-research-env/RegimeAnalysisContentSeries/Models')

    # Execute:
    MARKOV_AR = MarkovAutoRegressiveModels()
    MARKOV_AR._fitTheModel('filardo', None)
    MARKOV_AR._saveDataFrames(saveDirectory=dataframesSaveDirectory)
    #MARKOV_AR._plotModelOutputFilter(plotsSaveDirectory, showIt=True)
    MARKOV_AR._plotModelOutputSmoother(plotsSaveDirectory, showIt=True)