import csv
import random
from typing import Dict, List, Tuple
from domino import Domino
from linked_list import ChickenFootLine, LineNode
from random import randrange

# Do not modify; this is used by the tests
class PossibleMove:
    def __init__(self, target_line: ChickenFootLine, target_line_name:str, domino:Domino) -> None:
        self.target_line = target_line
        self.target_line_name = target_line_name
        self.domino = domino

# Chicken Foot Dominos
class ChickenFoot:

    # num_players: the number of players playing the game
    # max_pips: the largest number of pips (dots) on a side of a domino
    def __init__(self, num_players: int, max_pips: int) -> None:
        self.num_players = num_players
        self.max_pips = max_pips

        

        # list of line heads
        self.lines : List[ChickenFootLine] = []

        # keeps track of which player's turn it is
        self.active_player : int = 0

    # Starts a game of dominos using the starting double number
    # starting_pips: the number of pips for the starting double domino (e.g. 7 would be passed for a 7-7 in the center)
    # dominos_dealt: a list of starting hand for all players, where each hand is a list of Domino objects.  
    def start_game(self, starting_pips:int, dominos_dealt: List[List[Domino]] = None) -> None:
        self.player_hands = dominos_dealt


        # turn the starting_pips integer value into a domino object
        beginning_domino = Domino(starting_pips, starting_pips)
        beginning_domino.set_open_value(starting_pips)
        beginning_node = LineNode(beginning_domino)

        # create 6 new chicken_foot_lines with each starting with the beginning domino (defined by starting_pips)
        self.priority_queue : List[ChickenFootLine] = [] 
        for n in range(0, 6):
            line = ChickenFootLine(beginning_node)
            self.lines.append(line)
            self.priority_queue.append(line)

        # priority queue will have 3 ChickenFootLines with each's start.first being the double domino


        
        

    # Finds and returns a list of PossibleMove objects representing possible moves that the current player can make
    # based on tiles in their hand and what is open on the board (see object definition above) 
    def find_moves(self) -> List[PossibleMove]:
        list : List[PossibleMove] = []

        if len(self.priority_queue) != 0: # if the priority queue is NOT EMPTY, return that
            line = self.priority_queue[0]
            for dom in self.player_hands[self.active_player]:
                    if line.first.domino.open_value in dom.value: 
                        list.append(PossibleMove(line, line.line_name, dom))
                        
        else:
            for line in self.lines: # if the priority queue IS EMPTY go through the ChickenFootLine heads
                for dom in self.player_hands[self.active_player]:
                    if line.first.domino.open_value in dom.value: 
                        list.append(PossibleMove(line, line.line_name, dom))
        return list


    
    # Draws the specified domino from the pile into the current player's hand
    # domino: the domino that the user picked from the pile.  
    def draw_domino(self, domino:Domino = None) -> Domino:
        self.player_hands[self.active_player].append(domino)
        return domino
    
    # Place specified domino on the head of the place linked list
    # domino: the domino to place
    # place: a linked list of dominos on a path on the board
    def place_domino(self, domino:Domino, place) -> None:
        if place.first.domino.is_double():
            self.priority_queue.remove(place)
        
        if domino.is_double(): # check if the domino is a double (a chickenfoot)
            # CHICKENFOOT!!!!!!!!!!!
            # add 3 lines to the priority queue with the double domino as self.first
            place.add(domino)
            self.priority_queue.append(place)
            for n in range(0, 2):
                line = ChickenFootLine(LineNode(domino), place.line_name)
                self.priority_queue.append(line)
                self.lines.append(line)
        
        else: # otherwise, just add the domino to that line.
            place.add(domino)
        

            

    # Moves on to the next player
    def end_turn(self) -> None:
        # cycles through the list of players (just indeces 0, 1, 2, ...)
        self.active_player += 1
        if self.active_player > self.num_players-1:
            self.active_player = 0

    # Return a list of strings that represent all paths on the board (same string as the target_line_name), 
    # with the center double of the board as the last one. Paths are represented with hyphens between numbers on a single domino, 
    # and | between dominos.  e.g. A path on a board with a double 12 in the center looks like this: 
    # "7-2|2-2|2-5|5-6|6-6|6-1|1-12|12-12"
    def get_board_paths(self) -> List[str]:
        # just go through the list of Linked Lists, and put the 
        # toStrings of each into a new list and then return it
        list : List[str] = []
        for line in self.lines:
            list.append(line.line_name)
        return list