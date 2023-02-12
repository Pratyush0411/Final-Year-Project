
from master import Master
from initializer import Initializer
from ant_colony import Ant_colony

cnt = 0
loops = 100


for i in range(loops):
    init = Initializer(num_task=20)
    mst = Master(initializer=init,iter_num = 15)
    print(f"Iter {i} Decntralized")

    mst.phase_1()
    
    mst.phase_2()

    print(f"Iter {i} Centralized")
    ac = Ant_colony(
        profits=init.profits, n_ants=20, n_iterations=150, decay=0.2, alpha=1, beta=0.5
    )
    ac.main(
        resource_host_bandwidth=init.resource_host_bandwidth,
        resource_host_storage=init.resource_host_storage,
        resource_host_comp=init.resource_host_comp,
        resource_task_bandwidth=init.resource_task_bandwidth,
        resource_task_storage=init.resource_task_storage,
        resource_task_comp=init.resource_task_comp,
    )
    
    if mst.nodes[0].ant_colony.best_prof >= ac.best_prof:
        cnt+=1
        
    
print("Percentage of times Decentralized was atleast as good as centralized")

print(f"{(cnt/loops)*100}%")
    
