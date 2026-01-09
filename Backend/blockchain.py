blockchain = []

def add_block(data):
    block = {
        "index": len(blockchain) + 1,
        "data": data
    }
    blockchain.append(block)
    print("Block Added:", block)  # This prints in terminal
