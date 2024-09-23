# GO Game

This project is a digital version of the classic board game GO, developed in Python using Pygame for the graphical user interface (GUI) and socket programming for multiplayer functionality.

## Features

- **Multiplayer Support**: Play against another player over a network connection.
- **Graphical User Interface**: Intuitive and responsive UI using Pygame.
- **Game Logic**: Implements core GO game mechanics, including placing stones, capturing, and scoring.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame library
- Basic understanding of socket programming

### Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd go-game
   ```

2. Install Pygame:
   ```bash
   pip install pygame
   ```

3. Run the server:
   ```bash
   python server.py
   ```

4. Run the client (in a separate terminal):
   ```bash
   python client.py
   ```

### How to Play

- The game is played on a 9x9 board.
- Players take turns placing their stones on the board.
- The objective is to capture the opponent's stones by surrounding them.
- Players can resign or pass their turn as needed.

## Code Overview

- **boardPygame.py**: Initialises the Pygame window and handles the drawing of the board and player interactions.
  
- **client.py**: Manages the client-side logic, including user input and communication with the server.

- **game.py**: Contains the game logic for validating and processing moves.

- **gologic.py**: Defines the player and board classes, managing the game state and stone placement.

- **server.py**: Sets up the server to handle connections from two players and manages the game flow.

## Key Concepts

- **Game Board**: The game board is represented as a 2D list where players can place their stones. The board state is updated and sent to both players after each move.

- **Player Classes**: Each player has attributes such as name, color, score, and methods for managing their moves and captures.

- **Network Communication**: The server manages connections and synchronises game state between players using socket programming.

## Future Improvements

- Enhance the UI with additional features like score tracking and move history.
- Implement advanced game rules (e.g., ko rule, scoring).
- Add an AI opponent for single-player mode.

## Acknowledgments

- Inspired by the traditional board game GO.
- Special thanks to the Pygame community for providing the resources needed for GUI development.
