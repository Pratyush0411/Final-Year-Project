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
            self.resource_host_bandwidth[i] = random.randint(50, 100)
            self.resource_host_storage[i] = random.randint(80, 200)
            self.resource_host_comp[i] = random.randint(60, 150)

        for i in range(n_task):
            self.resource_task_bandwidth[i] = random.randint(20, 60)
            self.resource_task_storage[i] = random.randint(20, 120)
            self.resource_task_comp[i] = random.randint(20, 90)

        self.profits = {}

        for i in range(n_task):

            for j in range(n_host):
                link = (i, j)
                self.profits[link] = random.randint(20, 100)
                
                
                
    def __init__(self, num_host = 6, num_task = 10) -> None:

        self.num_hosts = num_host
        
        self.num_task = num_task
        
        self.__init_profits(n_host=num_host, n_task=num_task)
        
        self.graph = {
            1: [0,2,4],
            0: [1,5,4],
            4: [0,1,3],
            5: [0,3,2],
            2: [1,3,5],
            3: [2,4,5]
        }
    