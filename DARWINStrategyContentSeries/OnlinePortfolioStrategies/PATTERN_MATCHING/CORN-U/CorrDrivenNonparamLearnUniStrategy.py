### First, we append the previous level to the sys.path var:
import sys, os, pickle
### We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))
import pandas as pd
import matplotlib.pyplot as plt

# Import mlfinlab module:
from mlfinlab.online_portfolio_selection.pattern_matching import *

class CorrDrivenNonparamLearnUniStrategy(object):

    def __init__(self):

        # Get the data:
        self.loadDirectory = os.path.expandvars('${HOME}/Desktop/quant-research-env/DARWINStrategyContentSeries/Data/ClosePricePortfolio.csv')
        self.saveDirectory = os.path.expandvars('${HOME}/Desktop/quant-research-env/DARWINStrategyContentSeries/OnlinePortfolioStrategies/PATTERN_MATCHING/CORN-U/')
        self.DF_CLOSE = self._loadTechnicalDataset()

    def _loadTechnicalDataset(self):

        # Load it:
        ASSET_UNIVERSE = pd.read_csv(self.loadDirectory, index_col=0, parse_dates=True, infer_datetime_format=True)
        print('¡Asset Universe file LOADED!')

        return ASSET_UNIVERSE

    def _generateAllocations(self):

        # Create object:
        self.window = 3
        self.rho = 0.2
        self.PA_STRAT = CORNU(window=self.window, rho=self.rho)

        # Allocate:
        self.PA_STRAT.allocate(self.DF_CLOSE, verbose=True)

        # Do prints:
        print('Weights head:')
        print(self.PA_STRAT.all_weights.head())
        print('Weights tail:')
        print(self.PA_STRAT.all_weights.tail())
        print('Portfolio Return:')
        print(self.PA_STRAT.portfolio_return)

        # Plot portfolio return:
        self._plotPortfolioReturn()

    def _saveWeights(self):

        self.PA_STRAT.all_weights.to_csv(self.saveDirectory + 'PortfolioWeights.csv')

    def _plotPortfolioReturn(self):

        # Create the figure:
        f1, ax = plt.subplots(figsize = (10,5))

        # Create the plots:
        ax.plot(self.PA_STRAT.portfolio_return, label='Portfolio Return')
        ax.grid(True)

        plt.grid(linestyle='dotted')
        plt.xlabel('Date', horizontalalignment='center', verticalalignment='center', fontsize=14, labelpad=20)
        plt.ylabel('Returns', horizontalalignment='center', verticalalignment='center', fontsize=14, labelpad=20)
        ax.legend(loc='best')
        plt.title(f'Portfolio returns for {self.PA_STRAT.__class__.__name__} strategy')
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
        f1.canvas.set_window_title('Online Portfolio Selection')

        # In PNG:
        plt.savefig(self.saveDirectory + 'PortfolioReturns.png')

        # Show:
        plt.show()   

    def _predictOutcome(self):
    
        pass

if __name__ == "__main__":

    OBJECT = CorrDrivenNonparamLearnUniStrategy()

    OBJECT._generateAllocations()

    OBJECT._saveWeights()

    OBJECT._predictOutcome()