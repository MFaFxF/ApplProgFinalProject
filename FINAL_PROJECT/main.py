from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from view.mainView import MainView
from viewModel.mainViewModel import MainViewModel

import sys

app = QApplication(sys.argv)

main_view_model = MainViewModel()
main_view = MainView(main_view_model)
print("MainView initialized with ViewModel.")
main_view.show()
print("MainView is now visible.")

sys.exit(app.exec_())
app.exec()