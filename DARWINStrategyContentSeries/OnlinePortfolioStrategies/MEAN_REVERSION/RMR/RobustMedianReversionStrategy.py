### First, we append the previous level to the sys.path var:
import sys, os, pickle
### We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))
import pandas as pd
import matplotlib.pyplot as plt

# Import mlfinlab module:
from mlfinlab.online_portfolio_selection.mean_reversion import *

class RobustMedianReversionStrategy(object):

    def __init__(self):

        # Get the data:
        self.loadDirectory = os.path.expandvars('${HOME}/Desktop/quant-research-env/DARWINStrategyContentSeries/Data/ClosePricePortfolio.csv')
        self.saveDirectory = os.path.expandvars('${HOME}/Desktop/quant-research-env/DARWINStrategyContentSeries/OnlinePortfolioStrategies/MEAN_REVERSION/RMR/')
        self.DF_CLOSE = self._loadTechnicalDataset()

    def _loadTechnicalDataset(self):

        # Load it:
        ASSET_UNIVERSE = pd.read_csv(self.loadDirectory, index_col=0, parse_dates=True, infer_datetime_format=True)
        print('¡Asset Universe file LOADED!')

        return ASSET_UNIVERSE

    def _saveWeights(self):

        self.PA_STRAT.all_weights.to_csv(self.saveDirectory + 'PortfolioWeights.csv')

    def _generateAllocations(self):

        # Create object:
        self.epsilon = 18
        self.n_iteration = 200
        self.window = 120
        self.tau = 0.001
        self.PA_STRAT = RMR(self.epsilon, self.n_iteration, self.window, tau=self.tau)

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
    
        '''So, let's say that today 2020-06-26 after the close of X market I get all the close data up to and including today, input that into the .allocate() method (without taking into account here that I could optimize the algorithm by just passing the window data for some implementations) and the .weights attribute would be the weights that are chosen for Monday start in this case (i.e. 2020-06-29).'''

        print('FINAL PORTFOLIO WEIGHTS PREDICTION :')
        print(f'{self.PA_STRAT.weights}')

        # Append last data > Synthetic close price previous to the close
        # NOTE: WITH QUANDL, WE WILL JUST NEED TO CALL THE API and get the last data point or all again.
        # NOTE: THEN, WE WILL JUST CALL .WEIGHTS ATT.
        # https://github.com/hudson-and-thames/mlfinlab/issues/408
        #newData = pd.Series([random.uniform(0, 1) for eachCol in range(self.DF_CLOSE.shape[1])], 
        #                    index=self.DF_CLOSE.columns, 
        #                    name=datetime.now()) # name=datetime.now().strftime("%Y-%m-%d"))
        #self.DF_CLOSE2 = self.DF_CLOSE.append(newData, verify_integrity=True)

if __name__ == "__main__":

    OBJECT = RobustMedianReversionStrategy()

    OBJECT._generateAllocations()

    OBJECT._saveWeights()

    OBJECT._predictOutcome()