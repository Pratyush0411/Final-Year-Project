
from master import Master
from initializer import Initializer
from ant_colony import Ant_colony

init = Initializer()
mst = Master(initializer=init,iter_num = 10)
print("--------------Decentralized Solution-----------------")

print("______________________________________Phase 1__________________________________________")
mst.phase_1()
mst.print()
print("______________________________________Phase 2__________________________________________")
mst.phase_2()
mst.print()

print("--------------Centralized solution-------------------")

ac = Ant_colony(
    profits=init.profits, n_ants=10, n_iterations=10, decay=0.2, alpha=0.85, beta=0.5
)

ac.main(
    resource_host_bandwidth=init.resource_host_bandwidth,
    resource_host_storage=init.resource_host_storage,
    resource_host_comp=init.resource_host_comp,
    resource_task_bandwidth=init.resource_task_bandwidth,
    resource_task_storage=init.resource_task_storage,
    resource_task_comp=init.resource_task_comp,
)
print(ac.best_prof)
