from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize QLabel
        self.snackbar = QLabel('Snackbar', self)
        self.snackbar.resize(self.snackbar.sizeHint())

        # Set initial position
        self.position_snackbar()

    def resizeEvent(self, event):
        # Call the parent class method
        QMainWindow.resizeEvent(self, event)

        # Reposition the snackbar
        self.position_snackbar()

    def position_snackbar(self):
        right_margin = 10  # set the right margin
        bottom_margin = 10  # set the bottom margin

        # Calculate new position
        new_x_position = self.width() - self.snackbar.width() - right_margin
        new_y_position = self.height() - self.snackbar.height() - bottom_margin

        # Move the QLabel to the new position
        self.snackbar.move(new_x_position, new_y_position)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
