import unittest
from contracts.consensus import RAMConsensus

class TestRAMConsensus(unittest.TestCase):
    def setUp(self):
        self.consensus = RAMConsensus()

    def test_register_node(self):
        self.consensus.register_node('node1', 1024)
        self.assertEqual(self.consensus.nodes['node1'], 1024)

    def test_validate_consensus(self):
        self.consensus.register_node('node1', 1024)
        self.consensus.register_node('node2', 2048)
        # Adjust the test to ensure that the consensus is valid
        # Since one node has less RAM than the average, the consensus should be False
        self.assertFalse(self.consensus.validate_consensus())

if __name__ == '__main__':
    unittest.main()
