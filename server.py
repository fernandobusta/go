import socket
import pickle
import time
import game
import gologic

s = socket.socket()
host = "10.33.66.145"
port = 9990

playerOne = 1
playerTwo = 2

playerConn = list()
playerAddr = list()      

# Game objects
board = gologic.Board(9) # Make 9 an input
black = gologic.Player("Black", 1)
white = gologic.Player("White", 2) 

def get_input_old(currentPlayer):
    
    valid_move = False
    
    while not valid_move:
        try:
            # Update the player turn
            nextPlayer = playerOne if currentPlayer == playerOne else playerTwo
            update_player_turn(nextPlayer)
            
            # Receive the move
            move_data = playerConn[currentPlayer - 1].recv(2048 * 10)
            
            # Coordinates are sent as a string of the form "x,y"
            move = move_data.decode().split(",")
            
            # Ensure move is valid and in correct format
            if len(move) == 2 and move[0].isdigit() and move[1].isdigit():
                move = [int(move[0]), int(move[1])]
                # Validate move
                valid_move = game.validate_move(move, currentPlayer)
            
                if valid_move:
                    # Let the client know the move was valid
                    playerConn[currentPlayer - 1].send("Valid".encode())
                    # Update the game matrix (board)
                    print("Player {} made a move: {}".format(currentPlayer, move))
                    board = game.process_move(move, currentPlayer)
                    # Send the board back to the players
                    update_board_for_all(board)
                    
                else:
                    error_message = "Invalid move, please try again"
                    playerConn[currentPlayer - 1].send(error_message.encode())

            else:
                error_message = "Invalid move format, please try again"
                playerConn[currentPlayer - 1].send(error_message.encode())
        except:
            playerConn[currentPlayer - 1].send("Error".encode())
            print("Error occured! Try again..")
        
def get_input(currentPlayer):
    if currentPlayer == playerOne:
        update_player_turn(playerOne)
        conn = playerConn[0]
    else:
        update_player_turn(playerTwo)
        conn = playerConn[1]
        
    try:
        conn.send("Input".encode())
        valid_move = False
        
        while not valid_move:    
            data = conn.recv(2048 * 10)
            conn.settimeout(20)
            dataDecoded = data.decode().split(",")
            move = [int(dataDecoded[0]), int(dataDecoded[1])]
            
            # Validate the move
            valid_move = game.validate_move(move, currentPlayer)
            if valid_move:
                # Let the client know the move was valid
                conn.send("Valid".encode())
                # Update the game matrix (board)
                print("Player {} made a move: {}".format(currentPlayer, move))
                board = game.process_move(move, currentPlayer)
                update_board_for_all(board)
            else:
                error_message = "Error: Invalid move, please try again"
                conn.send(error_message.encode())
    except:
        conn.send("Error".encode())
        print("Error occured! Try again..")
    # LEFT IT HERE:
    # HAVE TO TEST THE FUNCTION
            

#Socket program
def start_server():
    #Binding to port 9999
    #Only two clients can connect 
    try:
        s.bind((host, port))
        print("GO server started \nBinding to port", port)
        s.listen(2) 
        accept_players()
    except socket.error as e:
        print("Server binding error:", e)


#Accept player
#Send player number
def accept_players():
    try:
        for i in range(2):
            conn, addr = s.accept()
            msg = "<<< You are player {} >>>".format(i+1)
            conn.send(msg.encode())

            playerConn.append(conn)
            playerAddr.append(addr)
            print("Player {} - [{}:{}]".format(i+1, addr[0], str(addr[1])))
    
        start_game()
        s.close()
    except socket.error as e:
        print("Player connection error", e)
    except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            exit()
    except Exception as e:
        print("Error occurred:", e)


def start_game_old():
    result = 0
    i = 0
    
    while result == 0:
        if (i%2 == 0):
            get_input(playerOne)
        else:
            get_input(playerTwo)
        # Just for testing, it should end once a player resigns
        if i == 10:
            result = 1
        i = i + 1
    
    send_common_msg("Over")

    if result == 1:
        lastmsg = "The winner is: Player One!!"
    elif result == 2:
        lastmsg = "The winner is: Player Tow!!"
    else:
        lastmsg = "Draw game!! Try again later!"

    send_common_msg(lastmsg)
    time.sleep(10)
    for conn in playerConn:
        conn.close()

def start_game():
    global board
    global black, white
    i = 1
    while not white.getResign() and not black.getResign() and (not white.getPass() or not black.getPass()):
        if i % 2 == 0:
            # White player's turn
            get_input(white.getColour())
        else:
            # Black player's turn
            get_input(black.getColour())
        i += 1


def send_common_msg(text):
    playerConn[0].send(text.encode())
    playerConn[1].send(text.encode())
    time.sleep(1)

def update_board_for_all(board):
    board_message = "Updated Board: " + str(board)
    for conn in playerConn:
        conn.send(board_message.encode())
    time.sleep(1)

def update_player_turn(currentPlayer):
    # Send the message about whose turn it is next
    turn_message = "Player {}'s Turn".format(currentPlayer)
    for conn in playerConn:
        conn.send(turn_message.encode())
    time.sleep(1)

start_server()