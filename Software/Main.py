from cProfile import label
#from msilib.schema import ComboBox
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from UserInterface import Ui_MainWindow
from Plotter import Plotter
from QueryHandler import QueryHandler
from QueryHandler import SmearHandler
from QueryHandler import StatfiHandler
from DataHandler import DataHandler

def main():
    if __name__ == "__main__":
        # Init queryhandlers:
        StatfiHandler1 = StatfiHandler()
        SmearHandler1 = SmearHandler()

        # Init dataHandler
        dataHandler = DataHandler(SmearHandler1, StatfiHandler1)

        # Init Plotter
        plotter = Plotter

        # Init UserInteface
        app = QtWidgets.QApplication(sys.argv)  
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow(dataHandler, plotter)
        ui.setupUi(MainWindow)

        #Connect "Plot" and "Save to Favorites" buttons with query saving functions, and fetch query parameters for them from datahandler
        ui.pushButton_Plot_Smear.released.connect(lambda: ui.addHistorySmear(dataHandler.getSmearParameters()))
        ui.pushButton_Plot_Statfi.released.connect(lambda: ui.addHistoryStatfi(dataHandler.getStatfiParameters()))
        ui.pushButton_SaveToFavorites.released.connect(lambda: ui.saveToFavoritesSmear(dataHandler.getSmearParameters()))
        ui.pushButton_SaveToFavorites.released.connect(lambda: ui.saveToFavoritesStatfi(dataHandler.getStatfiParameters()))
        #Add favorites on start up if there are any
        ui.addFavoritesSmear()
        ui.addFavoritesStatfi()

        #
        #
        #
        # Uncomment this to test merge:
        #
        #print(dataHandler.mergeSTATFI_SMEAR())

        MainWindow.show()
        sys.exit(app.exec_())

main()