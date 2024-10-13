
from typing import List
from unittest import TestCase
from chicken_foot import ChickenFoot
from domino import Domino

class Move:
    def __init__(self, line:str) -> None:
        items:list[str] = line.split(",")
        self.player = items[0].strip()
        self.move = items[1].strip()
        if len(items) > 2:
            domino_numbers = items[2].strip().split("-")
            self.domino = Domino(int(domino_numbers[0]), int(domino_numbers[1]))
        else:
            self.domino = None
        if len(items) > 3:
            self.place = items[3].strip()
        else:
            self.place = None

class ChickenFootTests(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def load_hands(self, domino_count, players) -> List[Domino]:
        handstrings = []
        with open(f"./tests/data/initial_hand_{domino_count}_{players}.txt", "r") as hand:
            handstrings = hand.readlines()
        hands = []
        for handstring in handstrings:
            dominos = []
            for domino in handstring.split("|"):
                numbers = domino.split("-")
                dominos.append(Domino(int(numbers[0]), int(numbers[1])))
            hands.append(dominos)
        return hands

    def load_plays(self, domino_count, players):
        moves = []
        with open(f"./tests/data/moves_{domino_count}_{players}.csv", "r") as move_reader:
            move = move_reader.readline()
            while(len(move) > 0):
                moves.append(Move(move))
                move = move_reader.readline()
        return moves

    def load_final_board(self, domino_count, players):
        paths = []
        with open(f"./tests/data/final_board_{domino_count}_{players}.txt", "r") as path_reader:
            path = path_reader.readline().strip()
            while(len(path) > 0):
                paths.append(path)
                path = path_reader.readline().strip()
        return paths

    def run_game(self, domino_count, players):
        hands = self.load_hands(domino_count,players) 
        plays:List[Move] = self.load_plays(domino_count,players)
        game = ChickenFoot(players, domino_count)
        game.start_game(domino_count, hands)
        for play in plays:
            moves = game.find_moves()
            if (play.move == "PLAY"):
                play_made = None
                for possible_play in moves:
                    if possible_play.target_line_name == play.place and possible_play.domino == play.domino:
                        play_made = possible_play
                        break
                game.place_domino(play_made.domino, play_made.target_line)
                game.end_turn()
            elif (play.move == "DRAW"):
                game.draw_domino(play.domino)
            else:
                game.end_turn()

        board = self.load_final_board(domino_count, players)
        current_paths = game.get_board_paths()
        self.assertEqual(len(board), len(current_paths))
        for current_path in current_paths:
            self.assertIn(current_path, board)

    def test_game_9_4(self):
        self.run_game(9, 4)
        
    def test_game_12_4(self):
        self.run_game(12, 4)
    
    def test_game_16_2(self):
        self.run_game(16, 2)
    
    def test_game_16_4(self):
        self.run_game(16, 4)
        
    def test_game_16_6(self):
        self.run_game(16, 6)
        