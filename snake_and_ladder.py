import random
class Snake:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Ladder:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Dice:
    def roll(self):
        val = random.randint(1, 6)
        return val 

class Player:
    def __init__(self, name):
        self.name = name
        self.current_position = 0

class Board:
    def __init__(self, size):
        self.snakes = []
        self.ladders = []
        self.size = size

    def add_snakes(self, start, end):
        self.snakes.append(Snake(start, end))
    
    def add_ladder(self, start, end):
        self.ladders.append(Ladder(start, end))
    
class Game:
    def __init__(self, board_size, players):
        self.board = Board(board_size)
        self.players = [Player(name) for name in players]
        self.current_player_index = 0
        self.dice = Dice()
    
    def add_snake(self, start, end):
        self.board.add_snakes(start, end)
    
    def add_ladder(self, start, end):
        self.board.add_ladder(start, end)
    
    def roll_dice_and_play(self):
        player = self.players[self.current_player_index]
        roll_dice = self.dice.roll()
        print(f"{player.name} rolled a {roll_dice}")
    
        player.current_position += roll_dice

        for snake in self.board.snakes:
            if player.current_position == snake.start:
                player.current_position = snake.end
                print(f"{player.name} encountered a snake! Moved to position {snake.end}")
        
        for ladder in self.board.ladders:
            if player.current_position == ladder.start:
                player.current_position = ladder.end
                print(f"{player.name} encountered a Ladder! Moved to position {ladder.end}")
        
        if player.current_position >= self.board.size:
            print(f"{player.name} wins!")

        self.current_player_index = (self.current_player_index + 1) % len(self.players)

if __name__ == '__main__':
    players = ["Player 1", "Player 2"]
    board_size = 20
    snake_and_ladder_game = Game(board_size, players)

    snake_and_ladder_game.add_snake(16, 6)
    snake_and_ladder_game.add_snake(47, 26)
    snake_and_ladder_game.add_ladder(4, 14)
    snake_and_ladder_game.add_ladder(49, 67)

    while True:
        snake_and_ladder_game.roll_dice_and_play()
        q = input("Press Enter to continue to the next turn... or enter 'q' to quit! - ")
        if q == 'q':
            break