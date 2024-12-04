class RAMConsensus:
    def __init__(self):
        self.nodes = {}

    def register_node(self, node_address, ram_usage):
        self.nodes[node_address] = ram_usage

    def validate_consensus(self):
        # Ensure there are nodes registered
        if not self.nodes:
            return False
        
        # Calculate the average RAM usage
        total_ram = sum(self.nodes.values())
        average_ram = total_ram / len(self.nodes)

        # print(f"Total RAM: {total_ram}")
        # print(f"Average RAM: {average_ram}")
        # print(f"Node RAM usages: {self.nodes.values()}")
        # Check if all nodes have at least the average RAM usage
        return all(ram >= average_ram for ram in self.nodes.values())
    
