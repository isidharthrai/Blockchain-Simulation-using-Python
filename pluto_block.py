import datetime as date
from block import Block

def create_pluto_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(1, date.datetime.now(), "Pluto Block", "1")
