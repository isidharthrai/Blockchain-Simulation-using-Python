import hashlib as hasher
import datetime as date

#importing the block
from block import Block

#importing the chain
import jupiter_block as jb
import pluto_block as pb
import neptune_block as nb


# Generate all later blocks in the blockchain
def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = last_block.data
  this_hash = last_block.hash
  return Block(this_index, this_timestamp, this_data, this_hash)

# Create the blockchain and add the genesis block
blockchain = [jb.create_jupiter_block(), pb.create_pluto_block(), nb.create_neptune_block()]

# How many blocks should we add to the chain
# after the genesis block
num_of_blocks_to_add = 1

# Add blocks to the chain
for i in range (len(blockchain)):
    previous_block = blockchain[i]
    for i in range(0, num_of_blocks_to_add):
        block_to_add = next_block(previous_block)
        blockchain.append(block_to_add)
        previous_block = block_to_add
        # Tell everyone about it!
        print("Block #{} added ".format(block_to_add.data))
        print("Hash: {}".format(block_to_add.hash))
        print("TimeStamp: {}".format(block_to_add.timestamp))
        print("Previous hash: {} \n".format(block_to_add.previous_hash))



