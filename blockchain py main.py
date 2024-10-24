import hashlib
import time
import json
import os

class Block:
    def __init__(self, index, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        value = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}".encode()
        return hashlib.sha256(value).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'data': self.data,
            'hash': self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.block_map = {}  # HashMap to store blocks by index for quick lookups
        self.hash_map = {}   # HashMap to store blocks by hash for quick lookups
        self.load_chain()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", time.time(), "Genesis Block")
        self.chain.append(genesis_block)
        self.block_map[genesis_block.index] = genesis_block  # Add to index hashmap
        self.hash_map[genesis_block.hash] = genesis_block    # Add to hash hashmap

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_index = previous_block.index + 1
        new_timestamp = time.time()
        new_block = Block(new_index, previous_block.hash, new_timestamp, data)
        self.chain.append(new_block)
        self.block_map[new_block.index] = new_block  # Add to index hashmap
        self.hash_map[new_block.hash] = new_block    # Add to hash hashmap

    def delete_block(self, index):
        if index >= len(self.chain) or index < 0:
            print("Invalid block index.")
            return
        
        if index == 0:
            print("Cannot delete the genesis block.")
            return
        
        # Remove the block and all subsequent blocks from both chain and hashmap
        for i in range(index, len(self.chain)):
            block_to_remove = self.chain[i]
            del self.hash_map[block_to_remove.hash]  # Remove from hash hashmap
        
        self.chain = self.chain[:index]  # Keep only blocks before the deleted block
        self.block_map = {block.index: block for block in self.chain}  # Rebuild index hashmap
        self.hash_map = {block.hash: block for block in self.chain}    # Rebuild hash hashmap
        print(f"Block {index} and all subsequent blocks have been deleted.")

    def display_chain(self):
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Timestamp: {time.ctime(block.timestamp)}")
            print(f"  Data: {block.data}")
            print(f"  Hash: {block.hash}\n")

    def save_chain(self):
        with open('blockchain.json', 'w') as file:
            json.dump([block.to_dict() for block in self.chain], file)

    def load_chain(self):
        if os.path.exists('blockchain.json'):
            with open('blockchain.json', 'r') as file:
                blocks = json.load(file)
                for block in blocks:
                    loaded_block = Block(block['index'], block['previous_hash'],
                                         block['timestamp'], block['data'])
                    loaded_block.hash = block['hash']  # Ensure the hash is also loaded
                    self.chain.append(loaded_block)
                    self.block_map[loaded_block.index] = loaded_block  # Add to index hashmap
                    self.hash_map[loaded_block.hash] = loaded_block    # Add to hash hashmap
        else:
            self.create_genesis_block()

    def block_exists(self, index):
        return index in self.block_map  # Check existence in index hashmap

    def find_block_by_hash(self, hash_value):
        return self.hash_map.get(hash_value, None)  # Return the block if found

if __name__ == "__main__":
    my_blockchain = Blockchain()

    while True:
        print("Options:")
        print("1. Add a new block")
        print("2. Check if a block exists by index")
        print("3. Find a block by hash")
        print("4. Display the blockchain")
        print("5. Delete a block")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            data = input("Enter data for the new block: ")
            my_blockchain.add_block(data)
            my_blockchain.save_chain()  # Save the blockchain after adding a block
            print("Block added!\n")

        elif choice == '2':
            index = int(input("Enter block index to check: "))
            if my_blockchain.block_exists(index):
                print(f"Block {index} exists in the blockchain.\n")
            else:
                print(f"Block {index} does not exist in the blockchain.\n")

        elif choice == '3':
            hash_value = input("Enter hash to find the block: ")
            block = my_blockchain.find_block_by_hash(hash_value)
            if block:
                print(f"Block found: {block.index}, Data: {block.data}, Hash: {block.hash}\n")
            else:
                print("Block not found.\n")

        elif choice == '4':
            print("Current Blockchain:")
            my_blockchain.display_chain()

        elif choice == '5':
            index = int(input("Enter block index to delete: "))
            my_blockchain.delete_block(index)
            my_blockchain.save_chain()  # Save the blockchain after deletion

        elif choice == '6':
            break

        else:
            print("Invalid option, please try again.")
