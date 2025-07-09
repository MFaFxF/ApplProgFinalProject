import sys
from PyQt5.QtWidgets import QApplication
from view.mainView import MainView
from viewModel.mainViewModel import MainViewModel


def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create the view model
    main_view_model = MainViewModel()

    # Create and show the main window
    main_window = MainView(main_view_model)
    main_window.show()
    # Run the application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()