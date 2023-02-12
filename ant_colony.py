import numpy as np
import copy
import math, random
from ant import Ant


class Ant_colony:
    def __init__(
        self, profits, n_ants, n_iterations, decay, alpha=1, beta=1, init_phermone=0.75
    ) -> None:

        self.n_ants = n_ants
        self.profits = profits
        self.phermones = {}
        self.incremental_phermones = {}
        for link in self.profits:
            self.phermones[link] = init_phermone
            self.incremental_phermones[link] = 0
        self.alpha = alpha
        self.beta = beta
        self.n_iterations = n_iterations
        self.decay = decay
        self.best_solution = []
        self.best_prof = 0

    def __update_phermone(
        self,
    ):

        for link in self.incremental_phermones:

            self.phermones[link] = ((1 - self.decay) * self.phermones[link]) + (
                self.incremental_phermones[link]
            )

    def __update_incremental_phermone(self, ant: Ant):

        for link in self.incremental_phermones:

            self.incremental_phermones[link] += ant.incremental_phermone[link]

    def merge_phermone(self, message_phermone_dict: dict, weight: int, host_ids:list):

        for link in self.phermones:
            inc = 0
            for host in host_ids:
                inc +=  (
                weight * message_phermone_dict[host][link]
            )
            self.phermones[link] = ((1 - self.decay) * self.phermones[link]) + inc

    def main(
        self,
        resource_host_storage,
        resource_host_comp,
        resource_host_bandwidth,
        resource_task_storage,
        resource_task_comp,
        resource_task_bandwidth,
    ):

        for i in range(self.n_iterations):
            tabu_list = []
            for j in range(self.n_ants):

                ant = Ant(
                    profits=self.profits,
                    resource_host_bandwidth=resource_host_bandwidth,
                    resource_host_storage=resource_host_storage,
                    resource_host_comp=resource_host_comp,
                    resource_task_bandwidth=resource_task_bandwidth,
                    resource_task_storage=resource_task_storage,
                    resource_task_comp=resource_task_comp,
                    alpha=self.alpha,
                    beta=self.beta,
                )
                while(True):
                    ant.perform_iter(self.phermones)
                    if ant.partial_solution not in tabu_list:
                        tabu_list.append(ant.partial_solution)
                        break
                    print(ant.partial_solution)
                    print("Repeating iteration for ant due to tabu_list hit")
                self.__update_incremental_phermone(ant)

                if ant.tot_profits >= self.best_prof:

                    self.best_solution = ant.partial_solution
                    self.best_prof = ant.tot_profits

            self.__update_phermone()

            # print(f"--------Iter {i+1}-----------")
            # print(self.phermones)
            # print(f"--------Total Profit-----------")
            # print(self.best_prof)


# Test 1
n_host = 10
n_task = 8
resource_host_storage = {}
resource_host_comp = {}
resource_host_bandwidth = {}
resource_task_storage = {}
resource_task_comp = {}
resource_task_bandwidth = {}
for i in range(n_host):
    resource_host_bandwidth[i] = random.randint(50, 100)
    resource_host_storage[i] = random.randint(80, 200)
    resource_host_comp[i] = random.randint(60, 150)

for i in range(n_task):
    resource_task_bandwidth[i] = random.randint(20, 60)
    resource_task_storage[i] = random.randint(20, 120)
    resource_task_comp[i] = random.randint(20, 90)

profits = {}
phermones = {}

for i in range(n_task):

    for j in range(n_host):
        link = (i, j)
        profits[link] = random.randint(20, 100)


ac = Ant_colony(
    profits=profits, n_ants=10, n_iterations=10, decay=0.2, alpha=0.5, beta=0.5
)

ac.main(
    resource_host_bandwidth=resource_host_bandwidth,
    resource_host_storage=resource_host_storage,
    resource_host_comp=resource_host_comp,
    resource_task_bandwidth=resource_task_bandwidth,
    resource_task_storage=resource_task_storage,
    resource_task_comp=resource_task_comp,
)
print(ac.best_prof)
print(ac.best_solution)