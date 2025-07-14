from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from mainView.mainViewNew import MainView
from mainViewModel.mainViewModel import MainViewModel

import sys

app = QApplication(sys.argv)

main_view_model = MainViewModel()
main_view = MainView(main_view_model)
print("MainView initialized with ViewModel.")
main_view.show()
print("MainView is now visible.")

sys.exit(app.exec_())
# main_view.update_data()  # Start updating data

app.exec()

if __name__ == "__main__":
    pass
    # mainViewModel = MainViewModel()
    # print("MainViewModel initialized, ready to process signals.")
    # mainViewModel.set_channel(10)  # Set initial channel
    # print("Channel set to:", mainViewModel.channel)