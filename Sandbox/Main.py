from cProfile import label
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from UserInterface import Ui_MainWindow
from Plotter import MplCanvas
from SMEARfunc import SMEARtest
from STATFIfunc import STATFItest
from QueryHandler import QueryHandler
from QueryHandler import SmearHandler
from QueryHandler import StatfiHandler

def main():
    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()

        sc = MplCanvas(Ui_MainWindow, width=5, height=4, dpi=100)
        sc2 = MplCanvas(Ui_MainWindow, width=5, height=4, dpi=100)

        # Init queryhandlers:
        StatfiHandler1 = StatfiHandler()
        SmearHandler1 = SmearHandler()

        # SMEAR query parameters:
        aggregation_type = 'MAX'
        interval_length = 60
        start_date = '2022-01-19T14:00:00.000'
        end_date = '2022-01-19T17:00:00.000'
        table_variable_name = 'VAR_EDDY.av_c'

        # Make SMEAR query using SmearHandler:
        SMEARx, SMEARy = SmearHandler1.Query(aggregation_type, interval_length, start_date, end_date, table_variable_name)

        # STATFI query parameters:
        items = ["Khk_yht_index", "Khk_yht_las_index"]
        years = ["2010", "2011"]

        # Make STATFI query using StatfiHandler:
        STATFIx, STATFIy = StatfiHandler1.Query(items, years)

        # Plot SMEAR data:
        sc.make_line_chart(SMEARx, SMEARy, ["Y Label 1", "Y Label 2"], [table_variable_name])
        # Plot STATFI data:
        sc2.make_line_chart(STATFIx, STATFIy, ["Y Label 1", "Y Label 2"], items)

        layout = QtWidgets.QVBoxLayout()
        layout2 = QtWidgets.QVBoxLayout()
        layout.addWidget(sc)
        layout2.addWidget(sc2)

        ui.widget_SmearPlot.setLayout(layout)
        ui.widget_StatfiPlot.setLayout(layout2)

        sys.exit(app.exec_())

main()