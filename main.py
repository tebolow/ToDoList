import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import *
from PyQt6 import uic
import os

tasksNames = []
tasksStatus = []
tasksPath = "my_tasks.txt"
darkFlag = False  # Global flag to track the current theme

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.applyLightTheme()  # Initialize with light theme
        uic.loadUi("GUI.ui", self)  # Load the UI from the .ui file
        self.listWidget = self.findChild(QListWidget, "listWidget")  # Find the QListWidget in the UI
        self.addBtn = self.findChild(QPushButton, "addBtn")
        self.addBtn.setIcon(QtGui.QIcon("media/plus_icon.svg"))  # Set icon for the Add button
        self.addBtn.setIconSize(QtCore.QSize(50, 50))
        self.addBtn.clicked.connect(self.goToCard)  # Connect Add button to goToCard method
        self.dark = self.findChild(QPushButton, "dark")
        self.dark.setIcon(QtGui.QIcon("media/dark_icon.svg"))  # Set icon for Dark Theme button
        self.dark.setIconSize(QtCore.QSize(50, 50))
        self.light = self.findChild(QPushButton, "light")
        self.light.setIcon(QtGui.QIcon("media/light_icon.svg"))  # Set icon for Light Theme button
        self.light.setIconSize(QtCore.QSize(50, 50))
        self.dark.clicked.connect(self.applyDarkTheme)  # Connect Dark button to applyDarkTheme method
        self.light.clicked.connect(self.applyLightTheme)  # Connect Light button to applyLightTheme method
        self.exitBtn = self.findChild(QPushButton, "exitBtn")
        self.exitBtn.clicked.connect(self.closeEvent)  # Connect Exit button to closeEvent method
        self.populateListWidget()  # Populate the list widget with tasks

    def goToCard(self):
        card = Card()
        widgetsStack.addWidget(card)  # Add the Card widget to the stack
        widgetsStack.setCurrentIndex(widgetsStack.currentIndex() + 1)  # Switch to the Card widget

    def populateListWidget(self):
        self.listWidget.clear()  # Clear existing items in the list widget
        for name, status in zip(tasksNames, tasksStatus):
            item = QListWidgetItem(self.listWidget)
            item.setSizeHint(QtCore.QSize(0, 45))  # Adjust item height

            widget = QWidget()
            layout = QHBoxLayout(widget)
            checkbox = QCheckBox(name)
            checkbox.setChecked(status == "True")  # Set checkbox state based on task status
            deleteBtn = QPushButton()
            deleteBtn.setIcon(QtGui.QIcon("media/bin_icon.svg"))  # Set icon for the Delete button
            deleteBtn.setIconSize(QtCore.QSize(25, 25))

            layout.addWidget(checkbox)
            layout.addWidget(deleteBtn)
            layout.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(layout)

            self.listWidget.setItemWidget(item, widget)

            # Connect checkbox and delete button signals
            checkbox.stateChanged.connect(lambda checked, n=name: self.updateStatus(checked, n))
            deleteBtn.clicked.connect(lambda _, n=name: self.deleteTask(n))

    def updateStatus(self, checked, name):
        index = tasksNames.index(name)
        tasksStatus[index] = "True" if checked else "False"
        write(tasksPath)  # Save updated task status to file

    def deleteTask(self, name):
        index = tasksNames.index(name)
        del tasksNames[index]
        del tasksStatus[index]
        write(tasksPath)  # Save updated tasks to file
        self.populateListWidget()  # Refresh the list widget

    def closeEvent(self, event):
        write(tasksPath)  # Save tasks to file on close
        event.accept()

    def applyDarkTheme(self):
        global darkFlag
        darkFlag = True
        self.applyTheme("media/QSS/ConsoleStyle.qss")  # Apply dark theme stylesheet

    def applyLightTheme(self):
        global darkFlag
        darkFlag = False
        self.applyTheme("media/QSS/MacOS.qss")  # Apply light theme stylesheet

    def applyTheme(self, themeFile):
        with open(themeFile, "r") as file:
            qss = file.read()
            self.setStyleSheet(qss)  # Apply stylesheet to main window
            # Apply the same stylesheet to all child widgets
            for widget in self.findChildren(QWidget):
                widget.setStyleSheet(qss)

class Card(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("card.ui", self)
        self.taskName = self.findChild(QTextEdit, "taskName")
        self.done = self.findChild(QPushButton, "done")
        self.done.clicked.connect(self.backToMainWindow)
        self.applyCurrentTheme()  # Apply current theme to Card widget

    def backToMainWindow(self):
        name = self.taskName.toPlainText().strip()
        if name:  # Only add the task if the name is not empty
            task = Task(name, False)
            task.addTask()
            window.populateListWidget()  # Refresh the list widget
            widgetsStack.setCurrentIndex(0)  # Return to the main window
        else:
            QMessageBox.warning(self, "Warning", "Task name cannot be empty!")  # Show warning if name is empty

    def applyCurrentTheme(self):
        if darkFlag:
            self.applyTheme("media/QSS/ConsoleStyle.qss")
        else:
            self.applyTheme("media/QSS/MacOS.qss")

    def applyTheme(self, themeFile):
        with open(themeFile, "r") as file:
            qss = file.read()
            self.setStyleSheet(qss)  # Apply stylesheet to Card widget

class Task:
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def addTask(self):
        tasksNames.append(self.name)
        tasksStatus.append(self.status)  # Add task to the list

def read(path):
    if not os.path.exists(path):
        open(path, 'w').close()  # Create an empty file if it does not exist
        return

    with open(path, "r") as file:
        for line in file:
            name, status = line.strip().split('|')
            tasksNames.append(name)
            tasksStatus.append(status)  # Read tasks from file

def write(path):
    with open(path, "w") as file:
        for name, status in zip(tasksNames, tasksStatus):
            file.write(f"{name}|{status}\n")  # Write tasks to file

app = QApplication(sys.argv)

read(tasksPath)  # Load tasks from file
widgetsStack = QtWidgets.QStackedWidget()
window = Window()
widgetsStack.addWidget(window)
widgetsStack.setFixedWidth(800)
widgetsStack.setFixedHeight(600)
widgetsStack.show()

app.exec()