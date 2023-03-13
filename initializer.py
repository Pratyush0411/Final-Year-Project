import random
from graph_generator import Graph

class Initializer:
    def __init_profits(self, n_host, n_task):

        self.resource_host_storage = {}
        self.resource_host_comp = {}
        self.resource_host_bandwidth = {}
        self.resource_task_storage = {}
        self.resource_task_comp = {}
        self.resource_task_bandwidth = {}
        self.deadline = {}

        phi = 10

        for i in range(n_host):
            self.resource_host_bandwidth[i] = int(random.uniform(150, 200))
            self.resource_host_storage[i] = int(random.uniform(150, 250))
            self.resource_host_comp[i] = int(random.uniform(100, 350))

        for i in range(n_task):
            self.resource_task_bandwidth[i] = int(random.uniform(10, 40))
            self.resource_task_storage[i] = int(random.uniform(10, 50))
            self.resource_task_comp[i] = int(random.uniform(10, 80))
            self.deadline[i] = phi * round(random.uniform(6, 10))

        self.profits = {}
        self.ending_time = {}
        for i in range(n_task):

            for j in range(n_host):
                link = (i, j)
                self.profits[link] = int(random.uniform(20, 100))
                self.ending_time[link] = phi * round(random.uniform(3, 8))

    def __init__(self, num_host=6, num_task=10, connection = "hard_coded") -> None:

        self.num_hosts = num_host

        self.num_task = num_task

        self.__init_profits(n_host=num_host, n_task=num_task)
        
        graph_gen = Graph(num_nodes=num_host, connection=connection)
        
        self.graph = graph_gen.graph

        #self.graph = {0: [2, 5], 1: [4], 2: [0, 3], 3: [2], 4: [5, 1], 5: [0, 4]}

    def test_ending_time_less_than_deadline(self, solution):

        for link in solution:

            task, host = link

            assert (
                self.ending_time[link] <= self.deadline[task]
            ), f"Deadline exceeded for task {task} deadline is {self.deadline[task]} and estimated ending time was {self.ending_time[link]}"

    def test_resources_not_exceeded(self, solution):

        resource_host_storage_consumed = {}
        resource_host_comp_consumed = {}
        resource_host_bandwidth_consumed = {}

        n_host = len(self.resource_host_bandwidth)

        for i in range(n_host):
            resource_host_bandwidth_consumed[i] = 0
            resource_host_storage_consumed[i] = 0
            resource_host_comp_consumed[i] = 0

        for link in solution:

            task, host = link
            resource_host_bandwidth_consumed[host] += self.resource_task_bandwidth[task]
            resource_host_comp_consumed[host] += self.resource_task_comp[task]
            resource_host_storage_consumed[host] += self.resource_task_storage[task]

        for host in range(n_host):

            assert (
                resource_host_bandwidth_consumed[host]
                <= self.resource_host_bandwidth[host]
            ), f"Bandwidth exceeded for host{host}"
            assert (
                resource_host_comp_consumed[host] <= self.resource_host_comp[host]
            ), f"COmputation exceeded for host{host}"
            assert (
                resource_host_storage_consumed[host] <= self.resource_host_storage[host]
            ), f"Storage exceeded for host{host}"

    def test_task_deployed_only_once(self, solution):

        tasks_deployed = [task for task, host in solution]

        tasks_deployed_set = set(tasks_deployed)

        assert len(tasks_deployed) == len(tasks_deployed_set), "Tasks not deployed once"
