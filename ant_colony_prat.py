import numpy as np
from copy import copy

class Ant_colony:
    
    def __init__(self,profits, n_ants, n_iterations, decay, alpha=1, beta=1) -> None:
        
        self.n_ants = n_ants
        self.profits = {}
        self.phermones = {}
        self.incremental_phermones = {}
        for link in self.profits:
            self.phermones[link] = 0.75
            self.incremental_phermones[link] = 0
         
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.best_solution = {}
        
    def __update_incremental_phermone(self, ):
        pass
        
    
    
class Ant:
    
    
    def __init__(self,profits, resource_host_storage, 
        resource_host_comp,
        resource_host_bandwidth ,
        resource_task_storage ,
        resource_task_comp ,
        resource_task_bandwidth ) -> None:
        
        self.profits = profits
        self.__create_local_copy(profits, resource_host_storage, 
        resource_host_comp,
        resource_host_bandwidth ,
        resource_task_storage ,
        resource_task_comp ,
        resource_task_bandwidth )
        
    def __init_iter(self,host_list,phermones):
        self.__create_consumed_dictionaries(host_list)
        self.phermones = phermones
        self.partial_solution= {}
        self.incremental_phermone = {}
        self.tot_profits = 0
        for link in self.profits:
            self.incremental_phermones[link] = 0
        
    
    def __create_consumed_dictionaries(self,host_list):
        
        for host in host_list:
            self.resource_host_storage_consumed[host] = 0
            self.resource_host_comp_consumed[host] = 0
            self.resource_host_bandwidth_consumed[host] = 0
        
        
    def __create_local_copy(self,profits, resource_host_storage, 
        resource_host_comp,
        resource_host_bandwidth ,
        resource_task_storage ,
        resource_task_comp ,
        resource_task_bandwidth ):
        
        self.resource_host_storage = copy.deepcopy(resource_host_storage)
        self.resource_host_comp = copy.deepcopy(resource_host_comp)
        self.resource_host_bandwidth = copy.deepcopy(resource_host_bandwidth)
        self.resource_task_storage = copy.deepcopy(resource_task_storage)
        self.resource_task_comp = copy.deepcopy(resource_task_comp)
        self.resource_task_bandwidth = copy.deepcopy(resource_task_bandwidth)
        
    def __search_feasible_links (self):
        
        links = []
        
        for task in self.resource_task_bandwidth:
            
            for host in self.resource_host_bandwidth:
                
                if self.resource_task_bandwidth[task] <= self.resource_host_bandwidth[host] and \
                    self.resource_task_storage[task] <= self.resource_host_storage[host] and \
                    self.resource_task_comp[task] <= self.resource_host_comp[host]:
                        
                        links.append((task,host))
                        
                        
    def __calculate_gamma (self, host_list):
        gamma_storage = {}
        gamma_comp = {}
        gamma_bandwidth = {}
        for host in host_list:
            
            gamma_storage[host] = self.resource_host_storage[host] - self.resource_host_storage_consumed[host]
            gamma_comp[host] = self.resource_host_comp[host] - self.resource_host_comp_consumed[host]
            gamma_bandwidth[host] = self.resource_host_bandwidth[host] - self.resource_host_bandwidth_consumed[host]
            
        return gamma_storage, gamma_bandwidth, gamma_comp
    
    
    def __calculate_local_heuristic(self):
        n_host = len(self.resource_host_bandwidth.keys)
        ita = {}
        gamma_storage, gamma_bandwidth, gamma_comp = self.__calculate_gamma(self.resource_host_bandwidth.keys)
        for link in self.partial_solution:
            task, host = link
            
            delta_storage = self.resource_task_storage[task]/(n_host*gamma_storage[host])
            delta_bandwidth = self.resource_task_bandwidth[task]/(n_host*gamma_bandwidth[host])
            delta_comp = self.resource_task_comp[task]/(n_host*gamma_comp[host])
            
            delta = (delta_bandwidth+delta_storage+delta_comp)/3
            
            if delta != 0:
                ita[link] = self.profits[link]/delta
            else:
                ita[link] = self.profits[link]/1
        
        return ita  
            
    def __update_incremental_phermone(self):
        
        # insert an increasing function later
        
        
        for link in self.partial_solution:
            
            self.incremental_phermone[link] = self.tot_profits
            
            
    def perform_iter(self,phermones):
        
        self.__init_iter( self.resource_host_comp.keys,phermones)
        
        feasable_link_set = self.__search_feasible_links()
        
        while(len(feasable_link_set)!=0):
            pass
            
            
        
        
        
        
        

        
            
        
        
        
        
            
            
        
        
        
        
                        
                        
    
                        
                    
                        
        
        
        
        
        
        
        
    