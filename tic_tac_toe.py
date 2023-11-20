class Board:
    def __init__(self, size=3):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
    
    def display(self):
        for row in self.grid:
            print('|'.join(row))
            print('-' * (2*self.size-1))

    def isFull(self):
        for row in self.grid:
            if ' ' in row:
                return False
        return True
    
    def place_piece(self, row, col, piece):
        if 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == ' ':
            self.grid[row][col] = piece
            return True
        return False 
    
    def isWinner(self, piece):
        # check rows
        for i in range(self.size):
            if all(self.grid[i][j] == piece for j in range(self.size)) or \
                    all(self.grid[j][i] == piece for j in range(self.size)):
                return True
                
        # check diagonals
        if all(self.grid[i][i] == piece for i in range(self.size)) or \
                all(self.grid[i][self.size - 1 - i] == piece for i in range(self.size)):
            return True
        
        return False            

class Player:
    def __init__(self, name, piece):
        self.name = name
        self.piece = piece
    
    def make_move(self, board):
        print(f"{self.name}'s turn ({self.piece})")
        row = int(input("Enter row index(0-based index): "))
        col = int(input("Enter column index(0-based index): "))
        if board.place_piece(row, col, self.piece):
            return True
        else:
            print("Invalid Input, Try again...")
            return self.make_move(board)
        

if __name__ == '__main__':
    board_size = int(input("Enter size of Board: "))
    board = Board(size = board_size)
    players = []
    pieces = ['X', 'O']
    num_of_players = int(input("Enter number of players: "))
    for i in range(num_of_players):
        name = input(f"Enter name of player {i+1}: ")
        piece = pieces[i]
        print(f"{name}, your piece is {piece}")
        players.append(Player(name, piece))
    
    current_player_index = 0
    while not board.isFull():
        current_player = players[current_player_index]
        board.display()
        if current_player.make_move(board):
           if board.isWinner(current_player.piece):
               board.display()
               print(f"{current_player.name} wins!")
               break
           else:
               current_player_index = (current_player_index + 1) % num_of_players
    else:
        board.display()
        print("It's a Draw!")
    
        
