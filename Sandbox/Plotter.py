import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import itertools

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.tight_layout()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

    # Plots the data given with line chart:
    def make_line_chart(self, x, y, unit, labels):
        # Plot data:
        # Case: 1 variable:
        if (len(y) == 1):
            # Plot the series:
            self.axes.plot(x, y[0], label = labels[0])
            # Add unit:
            self.axes.set_ylabel(unit[0])
        # Case: Multiple variables:
        else:
            # Plot the series:
            for i in range(len(y)):
                if (unit[i] != unit[0]):
                    # Set second axis if unit are different:
                    second_axis = self.axes.twinx()
                    # Plot the series:
                    second_axis.plot(x,y[i], label = labels[i], linestyle = '--')
                    # Add unit:
                    second_axis.set_ylabel(unit[i])
                    
                else:   
                    # Plot the series:
                    self.axes.plot(x,y[i], label = labels[i])
                    # Add unit:
                    self.axes.set_ylabel(unit[0])

        # Add legend:
        self.axes.legend(loc = 2)
        diff = max(list(itertools.chain.from_iterable(y))) - min(list(itertools.chain.from_iterable(y)))
        self.axes.set_ylim([min(list(itertools.chain.from_iterable(y))) - 0.1*diff, max(list(itertools.chain.from_iterable(y))) + 0.1*diff])
        if 'second_axis' in locals() or 'second_axis' in globals():
            second_axis.legend(loc = 1)
        
        

    # Plots the data given with bar chart:
    def make_bar_chart(self, x, y, unit, labels):

        # Set bar width:
        width = 0.2
        # Set x mark places using range of x labels:
        x_marks = [*range(1,(len(x)+1))]
        # Plot data:
        # Case: 1 variable:
        if (len(y) == 1):
            # Plot the x values to place:
            self.axes.bar(x_marks, y[0], width = width, label = labels[0])
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
            # Plot all y values:
            for i in range(len(y)):
                if (unit[i] != unit[0]):
                    # Set second axis if unit are different:
                    second_axis = self.axes.twinx()
                    # Move tick mark place on x axis as multiple series are plotted:
                    if i > 0:
                        x_marks = [r + width for r in x_marks]
                    # Plot the x values to place:
                    second_axis.bar(x_marks,y[i], width = width, label = labels[i])
                    # Set tick mark places on x axis:
                    second_axis.set_xticks([*range(1,(len(x)+1))], fontdict=None, minor=False)
                    # Set tick marks:
                    second_axis.set_xticklabels(x)
                    # Add unit:
                    second_axis.set_ylabel(unit[i])
                else:
                    # Move tick mark place on x axis as multiple series are plotted:
                    if i > 0:
                        x_marks = [r + width for r in x_marks]
                    # Plot the x values to place:
                    self.axes.bar(x_marks,y[i], width = width, label = labels[i])
                    # Set tick mark places on x axis:
                    self.axes.set_xticks([*range(1,(len(x)+1))], fontdict=None, minor=False)
                    # Set tick marks:
                    self.axes.set_xticklabels(x)
                    # Add unit:
                    self.axes.set_ylabel(unit[0])

        # Add legend:
                # Add legend:
        self.axes.legend(loc = 2)
        diff = max(list(itertools.chain.from_iterable(y))) - min(list(itertools.chain.from_iterable(y)))
        self.axes.set_ylim([min(list(itertools.chain.from_iterable(y))) - 0.1*diff, max(list(itertools.chain.from_iterable(y))) + 0.1*diff])
        
        if 'second_axis' in locals() or 'second_axis' in globals():
            second_axis.legend(loc = 1)