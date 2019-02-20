import datetime as date
from block import Block

def create_jupiter_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), "Jupiter Block", "0")
