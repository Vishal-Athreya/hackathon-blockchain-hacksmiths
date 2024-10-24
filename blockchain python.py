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
        self.load_chain()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", time.time(), "Genesis Block")
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_index = previous_block.index + 1
        new_timestamp = time.time()
        new_block = Block(new_index, previous_block.hash, new_timestamp, data)
        self.chain.append(new_block)

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
        else:
            self.create_genesis_block()

    def block_exists(self, index):
        return any(block.index == index for block in self.chain)

if __name__ == "__main__":
    my_blockchain = Blockchain()

    while True:
        print("Options:")
        print("1. Add a new block")
        print("2. Check if a block exists")
        print("3. Display the blockchain")
        print("4. Exit")
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
            print("Current Blockchain:")
            my_blockchain.display_chain()

        elif choice == '4':
            break

        else:
            print("Invalid option, please try again.")
