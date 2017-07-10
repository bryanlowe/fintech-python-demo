import sys
from PySide import QtGui
from gui import ClientInterface

def main():
    # start client app
    app = QtGui.QApplication(sys.argv)
    client_app = ClientInterface()
    client_app.launch()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()