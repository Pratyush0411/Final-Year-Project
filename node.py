
'''
Each host is a node or agent to run the distributed algorithm
'''
from timestamp import Timestamp
class Node:
    
    
    def __init__(self, N, M, host_id ) -> None:
        self.num_hosts = N
        self.num_tasks = M
        self.host_id = host_id
        self.phermone = {}
        self.neighbours = {}
        self.profits = {}
        self.message_queue = {}
        self.resource_host_storage = {}
        self.resource_host_comp = {}
        self.resource_host_bandwidth = {}
        self.resource_task_storage = {}
        self.resource_task_comp = {}
        self.resource_task_bandwidth = {}
        self.timestamp = Timestamp(self.num_hosts)        
    def send():
        
        pass
    
    def receive():
        
        pass
    
    def agree():
        
        pass
    
    
        
        