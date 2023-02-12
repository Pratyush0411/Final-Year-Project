import random

class Initializer:
    
    def __init_profits(self, n_host, n_task):

        self.resource_host_storage = {}
        self.resource_host_comp = {}
        self.resource_host_bandwidth = {}
        self.resource_task_storage = {}
        self.resource_task_comp = {}
        self.resource_task_bandwidth = {}
        
        for i in range(n_host):
            self.resource_host_bandwidth[i] = int(random.uniform(150, 200))
            self.resource_host_storage[i] = int(random.uniform(150, 250))
            self.resource_host_comp[i] = int(random.uniform(100, 350))

        for i in range(n_task):
            self.resource_task_bandwidth[i] = int(random.uniform(10, 40))
            self.resource_task_storage[i] = int(random.uniform(10, 50))
            self.resource_task_comp[i] = int(random.uniform(10, 80))

        self.profits = {}

        for i in range(n_task):

            for j in range(n_host):
                link = (i, j)
                self.profits[link] = int(random.uniform(20, 100))
                
                
                
    def __init__(self, num_host = 6, num_task = 10) -> None:

        self.num_hosts = num_host
        
        self.num_task = num_task
        
        self.__init_profits(n_host=num_host, n_task=num_task)
        
        # self.graph = {
        #     1: [0,2,4],
        #     0: [1,5,4],
        #     4: [0,1,3],
        #     5: [0,3,2],
        #     2: [1,3,5],
        #     3: [2,4,5]
        # }
        
        self.graph = {
            0:[2,5],
            1:[4],
            2:[0,3],
            3:[2],
            4:[5,1],
            5:[0,4]
            
        }
    