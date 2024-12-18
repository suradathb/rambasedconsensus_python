from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()
@app.route('/mine', methods=['GET'])
def mine():
    if len(blockchain.current_transactions) == 0:
        return jsonify({'message': 'No transactions to mine'}), 400

    validator = blockchain.select_validator()
    last_block = blockchain.last_block
    proof = 100
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'validator': validator
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    ram_usage = values.get('ram_usage')
    if nodes is None or ram_usage is None:
        return "Error: Please supply a valid list of nodes and RAM usage", 400
    for node in nodes:
        blockchain.register_node(node, ram_usage)
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/check_ram',methods=['GET'])
def check_ram():
    address = request.args.get('address')
    if address is None:
        return "Error: Please supply a  valid not address",400
    ram = blockchain.check_ram(address)
    if ram is not None:
        response = {
            'message': 'Node RAM found',
            'node': address,
            'ram': ram,
        }
        return jsonify(response),200
    else:
        return "Error: Node not found",400
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)