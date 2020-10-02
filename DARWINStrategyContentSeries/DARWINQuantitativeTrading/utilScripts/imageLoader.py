# Loading the image 
import pickle
import matplotlib.pyplot as plt
import os

def loadImage(imagePath, imageNb):

    candleFig = pickle.load(open(imagePath, 'rb'))
    candleFig.canvas.set_window_title(f'Image number > {imageNb}')
    
    print(f'PLOT - We are seeing image number: {imageNb}')
    plt.show()
    
if __name__ == '__main__':

    # Set directory:
    imageDirectory = os.path.expandvars('${HOME}/Desktop/quant-research-env/DARWINStrategyContentSeries/DARWINQuantitativeTrading/Plots/PickleFormat')

    # Loop it:
    for path, eachDirs, eachImages in os.walk(imageDirectory):

        print(f'Path: {path}')
        print(f'Dirs: {eachDirs}')
        print(f'Files: {eachImages}')

        for imageCounter, eachImg in enumerate(sorted(eachImages), 1):

            # Just exit each image to see the following one!
            filePath = os.path.join(path, eachImg)
            loadImage(filePath, imageCounter)
    
    print('PLOT - All images seen.')