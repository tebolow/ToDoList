# To-Do Application

## Overview

This is a simple To-Do application built with PyQt6, which allows users to manage tasks with a graphical user interface. Users can add, update, and delete tasks, and switch between light and dark themes. The application stores tasks in a text file and provides a basic UI for interacting with the tasks.

## Features

- **Add Tasks**: Create new tasks with a name and manage their status.
- **Delete Tasks**: Remove tasks from the list.
- **Update Status**: Mark tasks as completed or incomplete using checkboxes.
- **Switch Themes**: Toggle between light and dark themes.
- **Save and Load**: Tasks are saved to a text file and loaded when the application starts.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/tebolow/ToDoList.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd your-repo
   ```
   NOTE: change "your-repo" to your desired folder path.

3. **Install Dependencies**

   Ensure you have Python 3 and PyQt6 installed. You can install PyQt6 using pip:

   ```bash
   pip install PyQt6
   ```

## Usage

1. **Run the Application**

   ```bash
   python main.py
   ```

2. **Using the Application**

   - **Add Tasks**: Click the "+" button to create a new task.
   - **Delete Tasks**: Click the trash can icon next to a task to remove it.
   - **Update Task Status**: Check or uncheck the checkbox next to a task.
   - **Change Theme**: Click the "Dark" or "Light" button to switch themes.

## File Structure

- `main.py`: Main Python file that runs the application.
- `GUI.ui`: Qt Designer UI file for the main window.
- `card.ui`: Qt Designer UI file for the task creation card.
- `media/`: Directory containing media assets like icons and QSS files.
  - `icons/`: Icons for buttons and tasks.
  - `QSS/`: Qt Style Sheets for theming.
    - `ConsoleStyle.qss`: Dark theme stylesheet.
    - `MacOS.qss`: Light theme stylesheet.
- `my_tasks.txt`: Text file for storing tasks.

## Code Explanation

### `Window` Class

- **`__init__`**: Initializes the main window, sets up the UI, and connects buttons to their actions.
- **`goToCard`**: Opens the task creation card.
- **`populateListWidget`**: Populates the task list with existing tasks.
- **`updateStatus`**: Updates the status of a task.
- **`deleteTask`**: Deletes a task from the list.
- **`closeEvent`**: Saves tasks when the application is closed.
- **`applyDarkTheme`**: Applies the dark theme.
- **`applyLightTheme`**: Applies the light theme.
- **`applyTheme`**: Applies the specified theme stylesheet.

### `Card` Class

- **`__init__`**: Initializes the task creation card and applies the current theme.
- **`backToMainWindow`**: Adds the new task and returns to the main window if the task name is not empty.
- **`applyCurrentTheme`**: Applies the current theme based on the global dark flag.
- **`applyTheme`**: Applies the specified theme stylesheet.

### `Task` Class

- **`__init__`**: Initializes a task with a name and status.
- **`addTask`**: Adds the task to the global task lists.

### Functions

- **`read(path)`**: Reads tasks from the file.
- **`write(path)`**: Writes tasks to the file.
