import socket
import pygame
import threading
import time

s = socket.socket()
host = "10.33.66.145"
port = 9990

playerOne = 1
playerOneColor = (255, 255, 255) # White
playerTwo = 2
playerTwoColor = (0, 0, 0) # Black
bottomMsg = ""
msg = "Waiting for peer"
currentPlayer = 0
allow = 0 #allow handling mouse events
xy = (-1, -1)

BUTTON_POSITION = (100, 100)  # Adjust as needed
BUTTON_SIZE = (200, 50)       # Width and height
# Constants
GRID_SIZE = 9
CELL_SIZE = 40
board = [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((600, 550))  # Adjust the size as needed
pygame.display.set_caption("GO Game")

#fonts
bigfont = pygame.font.Font('freesansbold.ttf', 64)
smallfont = pygame.font.Font('freesansbold.ttf', 32)
backgroundColor = (0, 197, 255)
titleColor = (0, 0, 0)
subtitleColor = (128, 0, 255)

def create_thread(target):
    receive_thread = threading.Thread(target = target)
    receive_thread.daemon = True
    receive_thread.start()
    
def buildScreen(bottomMsg, string, playerColor = subtitleColor):
    screen.fill(backgroundColor)
    if "One" in string or "1" in string:
        playerColor = playerOneColor
    elif "Two" in string or "2" in string:
        playerColor = playerTwoColor
    # Define button properties
    button_color = (0, 128, 0)  # Green color
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 1:
                # Draw a black dot
                pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)
            elif board[row][col] == 2:
                # Draw a white dot
                pygame.draw.circle(screen, WHITE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)
            pygame.draw.line(screen, RED, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE), (col * CELL_SIZE + CELL_SIZE // 2, (row + 1) * CELL_SIZE), 1)
            pygame.draw.line(screen, RED, (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE // 2), ((col + 1) * CELL_SIZE, row * CELL_SIZE + CELL_SIZE // 2), 1)


    # Draw button
    button_rect = pygame.Rect(BUTTON_POSITION, BUTTON_SIZE)
    pygame.draw.rect(screen, button_color, button_rect)
    
    title = bigfont.render("Go Game", True, titleColor)
    screen.blit(title, (110, 0))
    subtitle = smallfont.render(str.upper(string), True, playerColor)
    screen.blit(subtitle, (150, 70))
    centerMessage(bottomMsg, playerColor)

    
def centerMessage(msg, color = titleColor):
    pos = (100, 480)
    if "One" in msg or "1" in msg:
        color = playerOneColor
    elif "Two" in msg or "2" in msg:
        color = playerTwoColor
    msgRendered = smallfont.render(msg, True, color)
    screen.blit(msgRendered, pos)

def handleMouseEvent_new(pos):
    # Constants for board layout (adjust these to match your board's layout and size)
    BOARD_SIZE = 19  # Size of the GO board (19x19)
    CELL_SIZE = 40   # Size of each cell in pixels
    BOARD_OFFSET = 50  # Offset from the edge of the window to the board

    # Calculate board coordinates from pixel coordinates
    board_x = (pos[0] - BOARD_OFFSET) // CELL_SIZE
    board_y = (pos[1] - BOARD_OFFSET) // CELL_SIZE

    # Check if the click is within the bounds of the board
    if 0 <= board_x < BOARD_SIZE and 0 <= board_y < BOARD_SIZE:
        return board_x, board_y
    else:
        print("Click outside the board")
        return None  # Return None or handle it as you see fit if the click is outside the board

def handleMouseEvent(pos, color):
    global xy
    clicked_row = pos[1] // CELL_SIZE
    clicked_col = pos[0] // CELL_SIZE
    
    # ... existing code to handle board clicks ...

    # Check if the click is on the button
    button_rect = pygame.Rect(BUTTON_POSITION, BUTTON_SIZE)
    if button_rect.collidepoint(pos):
        # Return a special coordinate or message
        xy = (3, 5)
        print("Button clicked!", xy)
    else:
        xy = (clicked_row, clicked_col)
    
def start_client():
    global currentPlayer
    global bottomMsg
    
    try:
        s.connect((host, port))
        print("Connected to: ", host, ":", port)
        recvData = s.recv(2048 * 10)
        bottomMsg = recvData.decode()
        # Determine player number
        if "1" in bottomMsg:
            currentPlayer = 1
        else:
            currentPlayer = 2

        # Run the game
        start_game()
        s.close()
    
    except socket.error as e:
        print("Socket connection error:", e)
        

def start_game():
    running = True
    global msg
    global bottomMsg
    global currentPlayer
    
    if currentPlayer == 1:
        color = playerOneColor
    else:
        color = playerTwoColor
        
    # Create a thread to receive messages
    create_thread(receive_server_messages)
    
    while running:
        # Get the button rectangle from buildScreen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if allow:
                    # Variable with the coordinates of the move
                    handleMouseEvent(pos, color)
        if msg == "":
            break
        
        buildScreen(bottomMsg, msg)
        pygame.display.update()

def receive_server_messages():
    global board
    global msg
    global bottomMsg
    global allow
    global xy
    while True:
        try:
            recvData = s.recv(2048 * 10)
            recvDataDecode = recvData.decode()
            buildScreen(bottomMsg, recvDataDecode)
            
            if recvDataDecode == "Input":
                failed = 1
                allow = 1
                xy = (-1, -1)
                while failed:
                    try: 
                        if xy != (-1, -1):
                            send_move_to_server(xy)
                            recvDataValidation = s.recv(2048 * 10)
                            recvDataValidationDecode = recvDataValidation.decode()
                            if recvDataValidationDecode == "Valid":
                                allow = 0
                                failed = 0
                            else:
                                print(recvDataValidationDecode)
                    except:
                        print("Error sending move to server")

            # Check if the received data is the updated board
            elif recvDataDecode.startswith("Updated Board: "):
                board = eval(recvDataDecode[len("Updated Board: "):])
                print("Received updated board from server:")
                print(board)  # This will just print the board representation to the terminal

            elif recvDataDecode == "Error":
                print("Error occured! Try again..")

            elif recvDataDecode == "Over":
                # Game has ended
                msgRecv = s.recv(2048 * 100) # receive the last message
                msgRecvDecoded = msgRecv.decode()
                bottomMsg = msgRecvDecoded
                msg = "~~~Game Over~~~"
                break
            else:
                # This is the board message
                print("else:", recvDataDecode)
                """ Messages here:
                - "<<< You are player {} >>>"
                - "Invalid move format, please try again"
                - "Invalid move, please try again"
                """
                msg = recvDataDecode
            
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            time.sleep(1)
            break

        except:
            print("Error occured")
            break
        

def send_move_to_server(move_coordinates):
    # Format the move as a string "x,y"
    move_str = "{},{}".format(move_coordinates[0], move_coordinates[1])

    try:
        # Send the move to the server
        s.send(move_str.encode())
    except Exception as e:
        print("Error sending move to server:", e)

start_client()