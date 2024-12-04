import requests
from flask import Flask, jsonify, request
import hashlib
import json
from time import time
import random

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.ram_stakes = {}

        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address, ram):
        self.nodes.add(address)
        self.ram_stakes[address] = ram

    def check_ram(self,address):
        # ตรวจสอบ RAM ที่ประกาศไว้ของโหนดที่ระบบ
        return self.ram_stakes.get(address,None)

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
        return True

    def slash_validator(self, validator):
        if validator in self.ram_stakes:
            del self.ram_stakes[validator]
            self.nodes.remove(validator)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False