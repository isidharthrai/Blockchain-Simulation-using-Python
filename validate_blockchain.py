import hashlib
s = hashlib.sha256()

from block import Block
import addBlock as add

def validate_blockchain(blockchain):

    for i in range (1,len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i-1]

        #current hash and calulated hash
        if ( current_block.hash != current_block.hash_block()):
            print ("Invalid Stage 1 error for Block {}".format(current_block.index))
            return False

        #previous hash validation
        if ( current_block.previous_hash != previous_block.hash):
            print ("Invalid Stage 2 error for Block {}".format(current_block.index))
            return False
    print("Valid at all stages")
    return True

validate_blockchain(add.blockchain)
