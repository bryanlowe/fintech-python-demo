import sys
from PySide import QtGui
from gui import ClientInterface

def main():
    app = QtGui.QApplication(sys.argv)
    guiObj = GUI()
    guiObj.launch()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()