# ⭕❌ Tic-Tac-Toe

> ☣ **Warning:** This project was created during my studies for educational purposes only. It may contain non-optimal solutions.

### 📝 About

A simple interactive game **Tic-Tac-Toe** has been implemented. The game is won by the player who places three of his symbols in one column, row or one of the diagonals. If no one has three pieces placed in this way and the board is filled - a draw occurs. 

> The application is written in **Python 3.10.9**, using the Qt Framework, in PyCharm 2023.1 (Professional Edition).

### 🪄 Functionality

In the graphical interface, you can find:
- Menu bar with two elements: **Game**, containing options **Start | Restart** and **Exit**, and **Info** with the option **About project**.
- **3x3 Board** with numbered tiles, where game takes place.
- **An icon** that shows which player is currently moving.
- **Field to enter movement** using the keyboard.
- **Players score**.
- **A clock** indicating the current time.

<img src="/_readme-img/1-main.png?raw=true 'Main window'" width="400">

The user can **change style** of the board and pieces by pressing the right mouse button. In the same way, the user can change an analog clock to a digital clock.

<img src="/_readme-img/2-style.png?raw=true 'Style'" width="400">

The player can **make a move** in one of three ways:
- Left-click on the selected tile.
- Enter the tile number in the input box and press Enter.
- Select the tile using the arrows on keyboard ( ← ↑ ↓ → ) and press Enter. To disable tile focus, press Backspace.

<img src="/_readme-img/3-focus.png?raw=true 'Focused tile'" width="400">

If one of the sides **wins** or **draws**, a notification window will be displayed, the scoring will be updated, and possibility of perfoming moves will be blocked (until players start a new game by clicking Game -> Start | Restart).
