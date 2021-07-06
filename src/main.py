"""
Main program entry file
"""
import sys

from PyQt5.QtWidgets import QApplication

import main_window


def main():
    """Main program enter point

    Returns:
        int: Return value which was set to QCoreApplication.exit()
    """
    app = QApplication(sys.argv)
    window = main_window.MainWindow()

    window.show()
    return app.exec_()


if __name__ == '__main__':
    main()
