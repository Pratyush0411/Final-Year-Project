from master import Master
from initializer import Initializer
from ant_colony import Ant_colony
import random, pickle, datetime

cnt = 0
loops = 10

decent_time_taken = []
decent_profit = []

cent_time_taken = []
cent_profit = []


def run_decentralized(init: Initializer):
    mst = Master(initializer=init, iter_num=10)
    print(f"Iter {i} Decentralized")

    mst.phase_1()

    mst.phase_2()

    return mst


def run_centralized(init: Initializer):
    print(f"Iter {i} Centralized")
    ct = Ant_colony(
        profits=init.profits,
        n_ants=20,
        n_iterations=100,
        decay=0.3,
        alpha=1,
        beta=1,
        deadline=init.deadline,
        ending_time=init.ending_time,
    )
    ct.main(
        resource_host_bandwidth=init.resource_host_bandwidth,
        resource_host_storage=init.resource_host_storage,
        resource_host_comp=init.resource_host_comp,
        resource_task_bandwidth=init.resource_task_bandwidth,
        resource_task_storage=init.resource_task_storage,
        resource_task_comp=init.resource_task_comp,
    )
    return ct


def check_solutions(init: Initializer, solution: list):

    init.test_ending_time_less_than_deadline(solution)
    init.test_resources_not_exceeded(solution)
    init.test_task_deployed_only_once(solution)


for i in range(loops):
    init = Initializer(num_task=10)

    st = datetime.datetime.now()
    mst = run_decentralized(init=init)
    et = datetime.datetime.now()
    
    decent_time = et-st
    decent_time_taken.append(decent_time)
    
    st = datetime.datetime.now()
    ct = run_centralized(init=init)
    et = datetime.datetime.now()

    cent_time = et-st
    cent_time_taken.append(cent_time)
    check_solutions(init, ct.best_solution)
    check_solutions(init, mst.nodes[0].ant_colony.best_solution)

    cent_profit.append(ct.best_prof)
    decent_profit.append(mst.nodes[0].ant_colony.best_prof)
    
    if mst.nodes[0].ant_colony.best_prof >= ct.best_prof:
        cnt += 1

    


print("Percentage of times Decentralized was better than centralized")

print(f"{(cnt/loops)*100}%")

print("_________Profits______________")
print("Decentralized algorithm:")
print(decent_profit)

print("Centralized algorithm:")
print(cent_profit)

print("_________Elapsed time______________")
print("Decentralized algorithm:")
print(decent_time_taken)

print("Centralized algorithm:")
print(cent_time_taken)

