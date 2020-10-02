### First, we append the previous level to the sys.path var:
import sys, os, pickle
### We append the repository path to the sys.path so that we can import packages easily.
sys.path.append(os.path.expandvars('${HOME}/Desktop/quant-research-env/'))
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

# Import mlfinlab module:
from mlfinlab.portfolio_optimization.herc import HierarchicalEqualRiskContribution

class HierarchicalEqualRiskContributionStrategy(object):

    def __init__(self):

        # Get the data:
        self.loadDirectory = os.path.expandvars('${HOME}/Desktop/quant-research-env/DARWINStrategyContentSeries/Data/ClosePricePortfolio.csv')
        self.saveDirectory = os.path.expandvars('${HOME}/Desktop/quant-research-env/DARWINStrategyContentSeries/OnlinePortfolioStrategies/_OPTIMIZATIONS/HERC/')
        self.DF_CLOSE = self._loadTechnicalDataset()

    def _loadTechnicalDataset(self):

        # Load it:
        ASSET_UNIVERSE = pd.read_csv(self.loadDirectory, index_col=0, parse_dates=True, infer_datetime_format=True)
        print('¡Asset Universe file LOADED!')

        return ASSET_UNIVERSE

    def _generateAllocations(self):

        # Create object:
        self.STRATEGY = HierarchicalEqualRiskContribution()

        # Allocate:
        self.STRATEGY.allocate(asset_names=self.DF_CLOSE.columns,
                               asset_prices=self.DF_CLOSE,
                               #risk_measure='expected_shortfall',
                               risk_measure='conditional_drawdown_risk', 
                               linkage='ward')

        # Plot portfolio metrics:
        self._plotOptimalPortfolio()
        self._plotClusters()

    def _plotOptimalPortfolio(self):

        print(f'Optimal number of clusters: {self.STRATEGY.optimal_num_clusters}')

        # Get weights:
        weights = self.STRATEGY.weights
        y_pos = np.arange(len(weights.columns))

        # Create the figure:
        f1, ax = plt.subplots(figsize = (10,5))

        # Create the plots:
        ax.bar(list(weights.columns), weights.values[0], label='Assets')
        plt.xticks(y_pos, rotation=45, size=10)
        plt.xticks(y_pos, rotation=45, size=10)
        ax.grid(True)

        plt.grid(linestyle='dotted')
        plt.xlabel('Assets', horizontalalignment='center', verticalalignment='center', fontsize=14, labelpad=20)
        plt.ylabel('Asset Weights', horizontalalignment='center', verticalalignment='center', fontsize=14, labelpad=20)
        ax.legend(loc='best')
        plt.title(f'Optimal portfolio for {self.STRATEGY.__class__.__name__} optimization')
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
        f1.canvas.set_window_title('OPTIMIZATION METHODS')

        # In PNG:
        plt.savefig(self.saveDirectory + 'OptimalPortfolio.png')

        # Show:
        plt.show()

    def _plotClusters(self):

        # Create the figure:
        f1, ax = plt.subplots(figsize = (10,5))

        # Create the plots:
        self.STRATEGY.plot_clusters(self.DF_CLOSE.columns)
        ax.grid(True)

        plt.grid(linestyle='dotted')
        plt.title(f'Dendrogram for {self.STRATEGY.__class__.__name__} optimization')
        plt.xticks(rotation=45)
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
        f1.canvas.set_window_title('OPTIMIZATION METHODS')

        # In PNG:
        plt.savefig(self.saveDirectory + 'Dendogram.png')

        # Show:
        plt.show()  

    def _predictOutcome(self):
    
        pass

if __name__ == "__main__":

    OBJECT = HierarchicalEqualRiskContributionStrategy()

    OBJECT._generateAllocations()

    OBJECT._predictOutcome()