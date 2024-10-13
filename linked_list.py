from typing import List
from domino import Domino

# The ChickenFootLine class is a specialized linked list for the game.  
class LineNode:
   def __init__(self, domino: Domino):
      self.next = None
      self.domino = domino


class ChickenFootLine:
   # chicken_foot is the domino that branches out
   def __init__(self, chicken_foot:LineNode, line_name:str = None) -> None:
      self.first = chicken_foot
      self.line_name = str(chicken_foot.domino)
      if line_name != None:
         self.line_name = line_name # line_name should be a string representing the entire line in the format "7-2|2-2|2-5|5-5", where last entry is the center

   def add(self, domino: Domino):
      node = LineNode(domino)
      domino.set_open_value(self.first.domino.open_value)
      node.next = self.first
      self.first = node
     
      # get the String of the domino you're adding and concatenate it to the front of the self.line_name
      self.line_name = str(domino) + "|" + self.line_name