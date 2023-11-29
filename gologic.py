class Player:
    """Represents a player in the Go game."""

    def __init__(self, name, colour):
        """Initialize a player with a name and stone colour."""
        self.name = name
        self.colour = colour
        self.score = 0
        self.captures = 0
        self.stoneGroups = []
        self.passTurn = False
        self.resign = False
        self.lastMove = 0

    def getName(self):
        """Get the name of the player."""
        return self.name

    def getScore(self):
        """Get the player's current score."""
        return self.score

    def getCaptures(self):
        """Get the number of opponent stones captured by the player."""
        return self.captures

    def getColour(self):
        """Get the colour of the player's stones."""
        return self.colour
    
    def getResign(self):
        """Get the colour of the player's stones."""
        return self.resign
    
    def getPass(self):
        """Get the colour of the player's stones."""
        return self.passTurn
    
    def resignGame(self):
        """Sets resign to true."""
        self.resign = True
        return 
    
    def playerPass(self):
        """Sets pass to true."""
        self.passTurn = True
        return
    
    def playerLastMove(self, move):
        """Stores previous move to prevent loops"""
        if move != self.lastMove:
            self.lastMove = move
            return True
        return False

    def resetPass(self):
        """Set pass back to false"""
        self.passTurn = False
        return

    # def calcTerritory(self):
    #     """Activated at the end of the game"""
    #     lst = [] 
    #     # List will store tuples of array coordinants
    #     # Search algorithm to find empty intersections contained in groups
    #     # returns the length if the list
    #     return len(lst)

    def addGroup(self, group):
        """Adds a new group to the players group list"""
        self.stoneGroups.append(group)
        return
    
    def removeGroup(self, group):
        """Remove a captured group instance from the players group list"""
        self.stoneGroups.remove(group)
        return
    
    def addBackLiberty(self, x, y, lst):
        """Add liberties from capturing a group"""
        newLst = self.findStoneGroups(lst)
        for stone in newLst:
            stone.addLiberty((x, y))
        return

    def findStoneGroups(self, stones):
        """Find what group a stone belongs to"""
        lst = []
        for stone in stones:
            for group in self.stoneGroups:
                if stone in group.getStones():
                    lst.append(group)
                    
        return list(set(lst))

    def combineGroups(self, cord, libertys, list):
        """Used to call merge group and delete all merged groups along with removing now covered liberties"""
        head = list[0]
        if len(list) > 1:
            for group in list[1:]:
                head.mergeGroups(group)
                self.stoneGroups.remove(group)
                del group
        head.addStone(cord, libertys)
        head.removeLiberty(cord)
        return
    
    def PlayerScore(self, teritory):
        """Calculates the players total score"""
        total = 0

        for group in self.stoneGroups:
            total += len(group.getStones())

        
        total += (teritory + self.captures)
         
        return total 
    
    def trackPlayerCaptures(self, n):
        """Updates each time a stone is captured"""
        self.captures += n
        return

    def getCaptures(self): #tmp
        return self.captures

class Board:
    """Represents the Go game board."""
    #ToDO create handlecaptures logic
        # loop move 
        # 

    def __init__(self, size):
        """Initialize the board with the specified size."""
        self.size = size
        # self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.liberty_list = []
        self.colour_list = []
        self.opponents = []
        self.grid = self.createGrid(size)

    def createGrid(self, n):
        nested_dict = {}
        for i in range(0, n ):
            inner_dict = {}
            for j in range(0, n):
                inner_dict[j] = 0
            nested_dict[i] = inner_dict
        return nested_dict

    def isLegalMove(self, x, y, colour):
        """This function will check if the player has made a valid placement"""
        if self.grid[x][y] != 0 or not self.checkAdjacent(x, y, colour):
            return False  # There is already a stone in the intersection

        # TODO: Add logic to check for suicide move and other rules
        # return checkAdjacent(self, x, y, colour)
        # Reset function 
        return True

    def placeStone(self, x, y, player):
        """Place a stone of the specified colour at the intersection."""
        if self.isLegalMove(x, y, player.getColour()) and player.playerLastMove((x, y)) :
            self.grid[x][y] = player.getColour()
            return True
        else:
            print("Cant place a stone there \n")
            return False
        # Update stone groups and liberties as needed
    
    def reset(self): # wipes the class variables
        """Wipes all the classes variables each round"""
        self.liberty_list = []
        self.colour_list = []
        self.opponents = []
        return

    def handleCaptures(self, cords, player, opponent):
        """This function will handle the capturing of territory on the board"""
        # updates the currents players captures
        # remove the stone from the array and set it back to 0
        if self.opponents:
            list = opponent.findStoneGroups(self.opponents) # Find the group classes that contain the stones in the list 
            for group in list:
                group.removeLiberty(cords) # Remove the opponents liberty that was captured from their group during currents move
                print(group.getLiberties()) # tmp 
                if not group.getLiberties(): # Of no liberties left capture the group
                    reset = group.getStones() 
                    for tuple in reset: # reset each cord back to 0 in the group
                        i,j = tuple
                        self.grid[i][j] = 0
                        self.reset()
                        self.checkAdjacent(i, j, player.getColour()) # Check what is around the cord
                        if self.colour_list: # If current has stones besided the cord
                            player.addBackLiberty(i, j, self.colour_list) # add a liberty to the stone group
                    player.trackPlayerCaptures(len(reset)) # add the captures to the player class
                    opponent.removeGroup(group) # Remove the captured stone from the opponents list
        return
        

    def checkAdjacent(self, x, y, colour):
        """Check all adjacent intersections to the placed stone."""
        cord = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

        for tuple in cord:
            i,j = tuple 
            if 0 <= i < self.size and 0 <= j < self.size: # Make sure its within the boards limits
                if self.grid[i][j] == 0:
                    self.liberty_list.append((i, j)) # Add a liberty
                elif self.grid[i][j] == colour:
                    self.colour_list.append((i, j)) # Add a stone of the same colour
                else:
                    self.opponents.append((i, j)) # Add an opponents stone

            
        return bool(self.liberty_list or self.colour_list) # Return whether it is or isnt a suicide move

    def getColourList(self):
        """Get the list of Stones of the same colour that are adjacent"""
        return self.colour_list

    def getLibertyList(self):
        """Get the list of liberties that are adjacent"""
        return self.liberty_list 

    def getSize(self):
        """Get the size of the Board group."""
        return self.size
    
    def getGrid(self):
        """Get the grid of the Board group."""
        return self.grid

class Group:
    """Represents a group of stones on the Go board."""

    def __init__(self, colour):
        """Initialize a stone group with a specified colour."""
        self.colour = colour
        self.stones = []  # List of Stone instances that belong to the group
        self.liberties = []  # List of group liberties 
        
    def getColour(self):
        """Get the colour of the stone group."""
        return self.colour

    def getLiberties(self):
        """Get the liberties of the stone group."""
        return self.liberties
    
    def getStones(self):
        """Get the stones of the stone group."""
        return self.stones

    def addStone(self, stone, liberties):
        """Add a stone to the group."""
        self.stones.append(stone)
        # Update the liberties of the group
        self.liberties.extend(liberties)
        self.liberties = list(set(self.liberties))
        return

    def addLiberty(self, liberty):
        """Add coordinates of a liberty to the list of liberties."""
        self.liberties.append(liberty)
        return

    def removeLiberty(self, liberty):
        """Remove coordinates of a liberty from the list of liberties."""
        if liberty in self.liberties:
            self.liberties.remove(liberty)
        return

    def mergeGroups(self, group):
        """Merge this group with another group."""
        if self.colour == group.colour:
            self.stones.extend(group.stones)
            # Update the liberties of the merged group
            self.liberties = list(set(self.liberties + group.liberties))  # Merge liberties and remove duplicates
        return

class Game:
    """Represents a game of Go."""

    def __init__(self, size):
        """Initialize a new game with a board and two players."""
        self.board = Board(size)
        self.b_player = Player("Jamie", 1)
        self.w_player = Player("Ferran", 2)

    def startNewGame(self):
        """Start a new game with the current players."""
        # Initialize the game state
        #creates a loop of commands to be ran for the game to function round by round
        i = 1
        while not self.w_player.getResign() and not self.b_player.getResign() and (not self.w_player.getPass() or not self.b_player.getPass()):
            grid_content = self.board.getGrid()
            for row in grid_content.values():
                print(*row.values())
            if i % 2 == 1:
                curr = self.b_player
                otherP = self.w_player
            else:
                curr = self.w_player
                otherP = self.b_player

            # user = input("Enter 1 to end game or 0 to continue: ") #tmp 
            # if int(user) > 0:
            #     curr.resignGame()

            self.board.reset()
            while True:
                useri = input("Please enter an integer: ")
                userj = input("Please enter an integer: ")
                x = int(useri)
                y = int(userj)
                if self.board.placeStone(x, y, curr):
                    break
            if self.board.getColourList():
                mergeList = curr.findStoneGroups(self.board.getColourList())
                curr.combineGroups((x, y), self.board.getLibertyList(), mergeList)
            else:
                newGroup = Group(curr.getColour())
                newGroup.addStone((x, y), self.board.getLibertyList())
                curr.addGroup(newGroup)
            self.board.handleCaptures((x, y), curr, otherP)
            i += 1


        #end  loop
        self.endGame() 
        return

    def endGame(self):
        """End the current game."""
        # Calculate and display the final score
        # bTeritory = b_player.calcTeritory()
        # wTeritory = w_player.calcTeritory()
        # # calculate all white stones in board
        # bScore = b_player.playerScore(bTeritory)
        # wScore = w_player.playerScore(wTeritory)

        # print(f"Player 1: {bScore} | Player 2: {wScore}")
        print("Game Over")

        return 
    
def main():
    newgame = Game(9)
    newgame.startNewGame()
    

if __name__ == "__main__":
    # Execute main function if this script is run directly
    main()


#todo
# Recapture territory
# loop moves - each player stores their last move , stops them repeating
# calc territory - find algorithm to calc territory  go cell by cell check if its a 0 , then get its liberties 
# player scores  - territory 
# if statement to resign   