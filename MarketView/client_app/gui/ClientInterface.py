import os
from PySide import QtCore, QtGui, QtWebKit
from datetime import datetime
from MarketView.client_app.utilities import NPD_DataSet


class ClientInterface(QtGui.QMainWindow):

    # Initialize the client interface
    def __init__(self):
        super(ClientInterface, self).__init__()

        # ui layout
        self.main_layout = QtGui.QGridLayout()
        self.menu_layout = QtGui.QHBoxLayout()
        self.menu_bar = QtGui.QMenuBar(self)

        # init filename
        self.file_name = None
        self.dataset = None

    # launches the client interface
    def launch(self):
        self.init_menu()
        self.setLayout(self.main_layout)
        self.setGeometry(300, 300, 1000, 700)
        self.setWindowTitle(" Market View ")
        self.show()

    def init_menu(self):
        # import button
        import_action = QtGui.QAction('&Import', self)
        import_action.triggered.connect(self.open_file)

        # exit button
        exit_action = QtGui.QAction('&Exit', self)
        exit_action.triggered.connect(self.close)

        # create file menu
        file_menu = self.menu_bar.addMenu('&File')
        file_menu.addAction(import_action)
        file_menu.addAction(exit_action)

        # set menu into layout
        self.menu_layout.addWidget(self.menu_bar)
        self.main_layout.addLayout(self.menu_layout, 0, 0)

    # opens a new file
    def open_file(self):
        # create file dialog
        file_dialog = QtGui.QFileDialog(self)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filters = "Data Files (*.xls *.xlsm *.xlsx)"
        self.file_name = file_dialog.getOpenFileName(self, 'Import Data File', dir_path, filters)[0]
        self.save_dataset()

    # opens a text field to save the dataset name. If cancel is pressed, the file_name is discarded
    def save_dataset(self):
        text, ok = QtGui.QInputDialog.getText(self, "Save Dataset", "Dataset:", QtGui.QLineEdit.Normal, (os.path.basename(self.file_name)+'_'+datetime.now().isoformat(timespec='minutes')))
        if ok and text:
           self.dataset = text
           self.setWindowTitle('{} - {}'.format(" Market View ", self.dataset))
           npd = NPD_DataSet(self.dataset)
           npd.set_data_file(self.file_name)
           if npd.clean_data():
               npd.save_report()
        else:
            self.file_name = None
            self.dataset = None
            self.setWindowTitle(" Market View ")
