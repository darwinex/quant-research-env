import pandas as pd
import itertools
import pprint

df = pd.read_csv('/home/eriz/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/CorrelationStudies/corrData.csv', index_col=0)

corrM = pd.read_csv('/home/eriz/Desktop/Darwinex/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/CorrelationStudies/corrMatrix.csv', index_col=0)

print(df.head())
print(corrM)

darwins = df.columns.to_list()
print(darwins)

darwinsComb = list(itertools.combinations(darwins, 2))
print(darwinsComb)

# For each combination: take two assets, get correlation and add it to a variable.
portfoliosDict = {}
corrDict = {}
corrDict2 = {}

for eachPortfolioIteration, eachCombination in enumerate(darwinsComb, 1):

    corrValueFinal = 0

    print(f'POSSIBLE PORTFOLIO: {eachCombination}')
    print(f'CORR VALUE FINAL (PRE-LOOP): {corrValueFinal}')
    darwinPairs = list(itertools.combinations(eachCombination, 2))

    for eachDarwinPair in darwinPairs:

        # Get the corr value:
        corrValue = corrM.loc[eachDarwinPair[0], eachDarwinPair[1]]

        # Add:
        corrValueFinal += corrValue

    # Print value final:
    print(f'CORR VALUE FINAL (AFTER LOOP): {corrValueFinal}')

    # Fill:
    portfoliosDict[eachPortfolioIteration] = eachCombination
    corrDict[eachPortfolioIteration] = corrValueFinal
    corrDict2[eachPortfolioIteration] = abs(corrValueFinal)

#pprint.pprint(portfoliosDict)
#pprint.pprint(corrDict)

print('#########################################')
pprint.pprint(corrDict)
pprint.pprint(corrDict2)
print('#########################################')
minKey = min(corrDict, key=corrDict.get)
print(f'VALUE: {corrDict[minKey]}')
print(f'PORTF: {portfoliosDict[minKey]}')
print('#########################################')
minKey2 = min(corrDict2, key=corrDict2.get)
print(f'VALUE: {corrDict2[minKey2]}')
print(f'PORTF: {portfoliosDict[minKey2]}')