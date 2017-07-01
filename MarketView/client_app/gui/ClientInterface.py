import os
from PySide import QtCore, QtGui, QtWebKit


class ClientInterface(QtGui.QWidget):

    # Initialize the client interface
    def __init__(self):
        super(ClientInterface, self).__init__()
        self.main_layout = QtGui.QGridLayout()
        self.unit_button_panel = QtGui.QVBoxLayout()
        # init button dict
        self.guiButtons = {}
        # init viewport dict
        self.guiViewPorts = {}
        # init chart viewport content
        self.chart_content = None
        # init report viewport content
        self.report_content = None
        # init filename
        self.file_name = None
        # init controller
        self.ctrl = Controller()