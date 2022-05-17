from cProfile import label
import sys
from turtle import clear
import matplotlib
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

#from DataHandler import DataHandler
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import itertools
from cycler import cycler
from numpy import random

class Plotter(FigureCanvasQTAgg):
    _dataHandler = "None"
    _width = 5
    _height = 4
    _dpi = 100
    
    def __init__(self, dataHandler):
        self._dataHandler = dataHandler
        self.fig = Figure(figsize=(self._width, self._height), dpi=self._dpi)
        self.fig.tight_layout()
        self.axes = self.fig.add_subplot(111)
        super(Plotter, self).__init__(self.fig)

    # Saves file as PNG:
    def save(self):
        # Open dialog to browse folders:
        fname = QFileDialog.getSaveFileName(self, 'Save File')
        # Save:
        if len(fname[0]) > 0:
            self.fig.savefig('{}'.format(fname[0]), dpi=200) 

    # Clear the figure:
    def clear(self):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)

    # A function to make bar chart
    def make_bar_chart(self, x, y, unit, labels):
    
        clear

        # Set bar width:
        width = 0.7/len(labels)
        # Set x mark places using range of x labels:
        x_marks = [*range(1,(len(x)+1))]
        # Plot data:
        # Case: 1 variable:
        if (len(y) == 1):
            # Plot the x values to place:
            self.axes.bar(x_marks, y[0], width = width, label = labels[0], color = ((random.random(), random.random(), random.random())))
            # Add unit:
            self.axes.set_ylabel(unit[0])
            # Set tick mark places on x axis:
            self.axes.set_xticks([*range(1,(len(x)+1))], minor=False)
            # Set tick marks:
            self.axes.set_xticklabels(x)
            # Add unit:
            self.axes.set_ylabel(unit[0])
        # Case: Multiple variables:
        else:
            units = list(set(unit))
            axes = []
            plots = []

            for i in range(len(units)-1):
                axes.append(self.axes.twinx())
                axes[i].spines["right"].set_position(("axes", i*1.0))

            # Plot all y values:
            for i in range(len(y)):
                if (unit[i] != unit[0]):
                    ax = units.index(unit[i])-1
                    # Move tick mark place on x axis as multiple series are plotted:
                    if i > 0:
                        x_marks = [r + width for r in x_marks]
                    # Plot the x values to place:
                    plt = axes[ax].bar(x_marks,y[i], width = width, label = labels[i], color = ((random.random(), random.random(), random.random())))
                    # Append plot:
                    plots.append(plt)
                    # Set tick mark places on x axis:
                    axes[ax].set_xticks([*range(1,(len(x)+1))], fontdict=None, minor=False)
                    # Set tick marks:
                    axes[ax].set_xticklabels(x)
                    # Add unit:
                    axes[ax].set_ylabel(unit[i])
                else:
                    # Move tick mark place on x axis as multiple series are plotted:
                    if i > 0:
                        x_marks = [r + width for r in x_marks]
                    # Plot the x values to place:
                    plt = self.axes.bar(x_marks,y[i], width = width, label = labels[i], color = ((random.random(), random.random(), random.random())))
                    # Append plot:
                    plots.append(plt)
                    # Set tick mark places on x axis:
                    self.axes.set_xticks([*range(1,(len(x)+1))], fontdict=None, minor=False)
                    # Set tick marks:
                    self.axes.set_xticklabels(x)
                    # Add unit:
                    self.axes.set_ylabel(unit[0])
                
            self.axes.legend(plots, [p.get_label() for p in plots])
        
        # Add legend:
        # self.axes.legend(loc = 2)
        # diff = max(list(itertools.chain.from_iterable(y))) - min(list(itertools.chain.from_iterable(y)))
        # self.axes.set_ylim([min(list(itertools.chain.from_iterable(y))) - 0.1*diff, max(list(itertools.chain.from_iterable(y))) + 0.1*diff])
        # if 'second_axis' in locals() or 'second_axis' in globals():
        #     second_axis.legend(loc = 1)


    # A function to make line charts:
    def make_line_chart(self, x, y, unit, labels):

        clear
        # Case: 1 variable:
        
        if (len(y) == 1):
            # Plot the series:
            self.axes.plot(x, y[0], label = labels[0], c = ((random.random(), random.random(), random.random())))
            # Add unit:
            self.axes.set_ylabel(unit[0])
            self.axes.legend(loc = 2)
        # Case: Multiple variables:
        else:
            units = list(set(unit))
            axes = []
            plots = []

            for i in range(len(units)-1):
                axes.append(self.axes.twinx())
                axes[i].spines["right"].set_position(("axes", i*1.0))

            # Plot the series:
            for i in range(len(y)):
                if (unit[i] != units[0]):
                    ax = units.index(unit[i])-1
                    # Plot the series:
                    
                    plt ,= axes[ax].plot(x,y[i], label = labels[i], c = ((random.random(), random.random(), random.random())))
                    plots.append(plt)
                    # Add unit:
                    axes[ax].set_ylabel(unit[i])
                    
                else:   

                    # Plot the series:
                    plt ,= self.axes.plot(x,y[i], label = labels[i], c = ((random.random(), random.random(), random.random())))
                    plots.append(plt)
                    # Add unit:
                    self.axes.set_ylabel(unit[0])

            self.axes.legend(plots, [p.get_label() for p in plots])
        
        # Add legend:
        # self.axes.legend(loc = 2)
        # diff = max(list(itertools.chain.from_iterable(y))) - min(list(itertools.chain.from_iterable(y)))
        # self.axes.set_ylim([min(list(itertools.chain.from_iterable(y))) - 0.1*diff, max(list(itertools.chain.from_iterable(y))) + 0.1*diff])
        # if 'second_axis' in locals() or 'second_axis' in globals():
        #     second_axis.legend(loc = 1)
       



    # Plots the data given with bar chart - smear:
    def make_bar_chart_smear(self):

        x = self._dataHandler._SMEARx
        y = self._dataHandler._SMEARy
        unit = self._dataHandler._SMEARunits
        labels = self._dataHandler._SMEARlabels

        if (len(x)>0 and len(y)>0 and len(unit)>0 and len(labels)):
            self.make_bar_chart(x, y, unit, labels)

    # Plots the data given with bar chart - statfi:
    def make_bar_chart_statfi(self):

        x = self._dataHandler._STATFIx
        y = self._dataHandler._STATFIy
        unit = self._dataHandler._STATFIitems
        labels = self._dataHandler._STATFIitems

        if (len(x)>0 and len(y)>0 and len(unit)>0 and len(labels)):
            self.make_bar_chart(x, y, unit, labels)

    # Plots the data given with line chart - smear:
    def make_line_chart_smear(self):

        x = self._dataHandler._SMEARx
        y = self._dataHandler._SMEARy
        unit = self._dataHandler._SMEARunits
        labels = self._dataHandler._SMEARlabels

        if (len(x)>0 and len(y)>0 and len(unit)>0 and len(labels)):
            self.make_line_chart(x, y, unit, labels)

    # Plots the data given with line chart - statfi:
    def make_line_chart_statfi(self):

        x = self._dataHandler._STATFIx
        y = self._dataHandler._STATFIy
        unit = self._dataHandler._STATFIitems
        labels = self._dataHandler._STATFIitems
        
        if (len(x)>0 and len(y)>0 and len(unit)>0 and len(labels)):
            self.make_line_chart(x, y, unit, labels)

    # Merges smear data on statfi data
    def mergeSMEAR_on_STATFI(self, line, bar):
        x, y, unit, labels = self._dataHandler.mergeSMEAR_on_STATFI()

        if (len(x)>0 and len(y)>0 and len(unit)>0 and len(labels)):
            if line:
                self.make_line_chart(x, y, unit, labels)
            elif bar:
                self.make_bar_chart(x, y, unit, labels)

    # Merges statfi data on smear data:
    def mergeSTATFI_on_SMEAR(self, line, bar):
        x, y, unit, labels = self._dataHandler.mergeSTATFI_on_SMEAR()

        if (len(x)>0 and len(y)>0 and len(unit)>0 and len(labels)):
            if line:
                self.make_line_chart(x, y, unit, labels)
            elif bar:
                self.make_bar_chart(x, y, unit, labels)



        

