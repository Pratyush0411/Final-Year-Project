import copy, random, math
import numpy as np


class Ant:
    def __init__(
        self,
        profits,
        resource_host_storage,
        resource_host_comp,
        resource_host_bandwidth,
        resource_task_storage,
        resource_task_comp,
        resource_task_bandwidth,
        alpha=1,
        beta=1,
    ) -> None:

        self.profits = profits
        self.__create_local_copy(
            profits,
            resource_host_storage,
            resource_host_comp,
            resource_host_bandwidth,
            resource_task_storage,
            resource_task_comp,
            resource_task_bandwidth,
        )
        self.alpha = alpha
        self.beta = beta

    def __init_iter(self, host_list, phermones):
        self.__create_consumed_dictionaries(host_list)
        self.phermones = phermones
        self.partial_solution = []
        self.incremental_phermone = {}
        self.tot_profits = 0
        self.deployed = {}
        for link in self.profits:
            task, host = link
            self.incremental_phermone[link] = 0
            if task not in self.deployed:
                self.deployed[task] = 0

    def __create_consumed_dictionaries(self, host_list):

        self.resource_host_storage_consumed = {}
        self.resource_host_comp_consumed = {}
        self.resource_host_bandwidth_consumed = {}

        for host in host_list:
            self.resource_host_storage_consumed[host] = 0
            self.resource_host_comp_consumed[host] = 0
            self.resource_host_bandwidth_consumed[host] = 0

    def __create_local_copy(
        self,
        profits,
        resource_host_storage,
        resource_host_comp,
        resource_host_bandwidth,
        resource_task_storage,
        resource_task_comp,
        resource_task_bandwidth,
    ):

        self.resource_host_storage = copy.deepcopy(resource_host_storage)
        self.resource_host_comp = copy.deepcopy(resource_host_comp)
        self.resource_host_bandwidth = copy.deepcopy(resource_host_bandwidth)
        self.resource_task_storage = copy.deepcopy(resource_task_storage)
        self.resource_task_comp = copy.deepcopy(resource_task_comp)
        self.resource_task_bandwidth = copy.deepcopy(resource_task_bandwidth)

    def __search_feasible_links(self):

        links = []

        for task in self.resource_task_bandwidth:

            for host in self.resource_host_bandwidth:

                if (
                    self.resource_task_bandwidth[task]
                    <= (
                        self.resource_host_bandwidth[host]
                        - self.resource_host_bandwidth_consumed[host]
                    )
                    and self.resource_task_storage[task]
                    <= (
                        self.resource_host_storage[host]
                        - self.resource_host_storage_consumed[host]
                    )
                    and self.resource_task_comp[task]
                    <= (
                        self.resource_host_comp[host]
                        - self.resource_host_comp_consumed[host]
                    )
                    and (self.deployed[task] == 0)
                ):

                    links.append((task, host))
                    

        return links

    def __calculate_gamma(self, host_list):
        gamma_storage = {}
        gamma_comp = {}
        gamma_bandwidth = {}
        for host in host_list:

            gamma_storage[host] = (
                self.resource_host_storage[host]
                - self.resource_host_storage_consumed[host]
            )
            gamma_comp[host] = (
                self.resource_host_comp[host] - self.resource_host_comp_consumed[host]
            )
            gamma_bandwidth[host] = (
                self.resource_host_bandwidth[host]
                - self.resource_host_bandwidth_consumed[host]
            )

        return gamma_storage, gamma_bandwidth, gamma_comp

    def __calculate_local_heuristic(self):
        n_host = len(self.resource_host_bandwidth.keys())
        ita = {}
        gamma_storage, gamma_bandwidth, gamma_comp = self.__calculate_gamma(
            self.resource_host_bandwidth.keys()
        )
        delta = {}

        for link in self.profits:

            task, host = link
            if (
                gamma_storage[host] == 0
                or gamma_comp[host] == 0
                or gamma_bandwidth[host] == 0
            ):
                if task not in delta:
                    delta[task] = 0
            else:
                delta_storage = self.resource_task_storage[task] / (
                    n_host * gamma_storage[host]
                )
                delta_bandwidth = self.resource_task_bandwidth[task] / (
                    n_host * gamma_bandwidth[host]
                )
                delta_comp = self.resource_task_comp[task] / (n_host * gamma_comp[host])
                if task not in delta:
                    delta[task] = 0
                delta[task] += (delta_bandwidth + delta_storage + delta_comp) / (
                    3 * n_host
                )

        for link in self.profits:
            task, _ = link
            ita[link] = self.profits[link] / delta[task]

        return ita

    def __update_incremental_phermone(self):

        # insert an increasing function later

        for link in self.partial_solution:

            self.incremental_phermone[link] = math.sqrt(self.tot_profits)

    def __calculate_prob_matrix(self, allowed_links: list):

        denom = 0
        local_heuristic = self.__calculate_local_heuristic()

        for link in allowed_links:

            denom += (math.pow(self.phermones[link], self.alpha)) * (
                math.pow(local_heuristic[link], self.beta)
            )
        prob_list = []
        for link in allowed_links:
            prob = (
                (math.pow(self.phermones[link], self.alpha))
                * (math.pow(local_heuristic[link], self.beta))
            ) / denom
            prob_list.append(prob)

        return prob_list

    def __update_consumed_matrix(self, chosen_link):
        task, host = chosen_link

        self.resource_host_bandwidth_consumed[host] += self.resource_task_bandwidth[
            task
        ]
        self.resource_host_comp_consumed[host] += self.resource_task_comp[task]
        self.resource_host_storage_consumed[host] += self.resource_task_storage[task]

    def perform_iter(self, phermones):

        self.__init_iter(self.resource_host_comp.keys(), phermones)

        feasable_link_set = self.__search_feasible_links()

        while len(feasable_link_set) != 0:

            prob_list = self.__calculate_prob_matrix(feasable_link_set)
            chosen_index = np.random.choice(range(len(feasable_link_set)), p=prob_list)

            chosen_link = feasable_link_set[chosen_index]
            task, _ = chosen_link
            self.partial_solution.append(chosen_link)
            self.deployed[task] = 1
            self.__update_consumed_matrix(chosen_link=chosen_link)
            self.tot_profits += self.profits[chosen_link]
            feasable_link_set = self.__search_feasible_links()

        self.__update_incremental_phermone()
