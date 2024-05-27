import hashlib

def calculate_block_hash(block_data):
    block_string = ""
    #print("block data :" ,block_data)
    for key in sorted(block_data.keys()):
        if key != 'current block hash':
            block_string += "{}:{};".format(key, block_data[key])
    return hashlib.sha256(block_string.encode()).hexdigest()