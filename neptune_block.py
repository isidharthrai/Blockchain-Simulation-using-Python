import datetime as date
from block import Block

def create_neptune_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(2, date.datetime.now(), "Neptune Block", "2")
