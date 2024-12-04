import hashlib
import json
from time import time
import random

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.ram_stakes = {}  # เก็บข้อมูลการ stake RAM ของแต่ละ node

        # สร้างบล็อก genesis
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address, ram):
        self.nodes.add(address)
        self.ram_stakes[address] = ram

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def select_validator(self):
        total_ram = sum(self.ram_stakes.values())
        pick = random.uniform(0, total_ram)
        current = 0
        for node, ram in self.ram_stakes.items():
            current += ram
            if current > pick:
                return node

    def validate_block(self, block):
        # ตรวจสอบธุรกรรมและบล็อก
        return True

    def slash_validator(self, validator):
        if validator in self.ram_stakes:
            del self.ram_stakes[validator]
            self.nodes.remove(validator)

    def resolve_conflicts(self):
        # กลไกฉันทามติ
        return False