import unittest
import json
from node import app, blockchain

class BlockchainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_mine(self):
        response = self.app.get('/mine')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('index', data)
        self.assertIn('transactions', data)
        self.assertIn('proof', data)
        self.assertIn('previous_hash', data)

    def test_new_transaction(self):
        transaction = {
            'sender': 'sender_address',
            'recipient': 'recipient_address',
            'amount': 5
        }
        response = self.app.post('/transactions/new', data=json.dumps(transaction), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_register_nodes(self):
        nodes = {
            'nodes': ['node1', 'node2'],
            'ram_usage': 1024
        }
        response = self.app.post('/nodes/register', data=json.dumps(nodes), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('total_nodes', data)

    def test_consensus(self):
        response = self.app.get('/nodes/resolve')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('chain', data)

if __name__ == '__main__':
    unittest.main()