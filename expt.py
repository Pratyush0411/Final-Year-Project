from master import Master
from initializer import Initializer
from ant_colony import Ant_colony
import random, pickle, datetime
from hyper_parameters import *
import pandas as pd


def run_decentralized(
    init: Initializer,
    hp_shuffle: bool = True,
    n_ants: int = 2,
    n_iter: int = 10,
    max_iter: int = 10,
):
    mst = Master(
        initializer=init,
        iter_num=max_iter,
        hp_shuffle=hp_shuffle,
        n_ants=n_ants,
        n_iter=n_iter,
    )
    print(f"Iter {i} Decentralized")

    mst.phase_1()

    mst.phase_2()

    return mst


def run_centralized(init: Initializer, n_ants: int = 20, n_iter: int = 100):
    print(f"Iter {i} Centralized")
    ct = Ant_colony(
        profits=init.profits,
        n_ants=n_ants,
        n_iterations=n_iter,
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
    print("All tests passed successfully")


expt_data = []

headers = [
    "Number of tasks",
    "Number of hosts",
    "Centralized ants",
    "Centralized iter",
    "Distributed ants",
    "Distributed iter",
    "Hyperparameter randomization",
    "Max allowed iter - Distributed",
    "Average time - Centralized",
    "Average time - Distributed",
    "Average profit - Centralized",
    "Average profit - Distributed",
    "Percent of times Distributed better profits",
    "Guarantee Ratio - Centralized",
    "Guarantee ration - Distributed"
]
max_time = len(ants_choice)*len(tasks_choice)*len(hosts_choice)*len(iter_choice)*len(decent_max_loops_choice)*len(decent_param_choice)*2
time_completed = 0
for n_tasks in tasks_choice:

    for n_hosts in hosts_choice:

        for cants in ants_choice:

            for citer in iter_choice:

                for dparam in decent_param_choice:

                    dants = int(dparam * cants)
                    diter = int(dparam * citer)

                    for hpshuffle in [False, True]:

                        for max_loop_percent in decent_max_loops_choice:
                            print(f"================= Percent of experiment completed {(time_completed*100)/max_time}-=========================")
                            max_iter = (citer // diter) * max_loop_percent
                            dcnt_better_than_cnt_count = 0
                            loops = 10

                            decent_time_taken = []
                            decent_profit = []

                            cent_time_taken = []
                            cent_profit = []
                            for i in range(loops):
                                init = Initializer(num_task=n_tasks, num_host=n_hosts)

                                st = datetime.datetime.now()
                                mst = run_decentralized(
                                    init=init,
                                    hp_shuffle=hpshuffle,
                                    n_ants=dants,
                                    n_iter=diter,
                                    max_iter=max_iter,
                                )
                                et = datetime.datetime.now()

                                decent_time = et - st
                                decent_time = int(decent_time.seconds) + round(
                                    decent_time.microseconds / (pow(10, 6)), 4
                                )
                                decent_time_taken.append(decent_time)

                                st = datetime.datetime.now()
                                ct = run_centralized(
                                    init=init, n_ants=cants, n_iter=citer
                                )
                                et = datetime.datetime.now()

                                cent_time = et - st
                                cent_time = int(cent_time.seconds) + round(
                                    cent_time.microseconds / (pow(10, 6)), 4
                                )
                                cent_time_taken.append(cent_time)
                                check_solutions(init, ct.best_solution)
                                check_solutions(
                                    init, mst.nodes[0].ant_colony.best_solution
                                )

                                cent_profit.append(ct.best_prof)
                                decent_profit.append(mst.nodes[0].ant_colony.best_prof)

                                if mst.nodes[0].ant_colony.best_prof >= ct.best_prof:
                                    dcnt_better_than_cnt_count += 1

                            avg_dcnt_prof = sum(decent_profit) / loops
                            avg_cnt_prof = sum(cent_profit) / loops

                            avg_cnt_time = sum(cent_time_taken) / loops
                            avg_dcnt_time = sum(decent_time_taken) / loops
                            
                            gr_cent = (len(ct.best_solution)/n_tasks) *100
                            gr_dcent = (len(mst.nodes[0].ant_colony.best_solution)/n_tasks) *100

                            dcnt_better_than_cnt_count = (
                                dcnt_better_than_cnt_count / loops
                            ) * 100
                            
                            data = [
                                n_tasks,
                                n_hosts,
                                cants,
                                citer,
                                dants,
                                diter,
                                hpshuffle,
                                max_iter,
                                avg_cnt_time,
                                avg_dcnt_time,
                                avg_cnt_prof,
                                avg_dcnt_prof,
                                dcnt_better_than_cnt_count,
                                gr_cent,
                                gr_dcent
                            ]
                            expt_data.append(data)
                            time_completed+= 1


expt_data_df = pd.DataFrame(expt_data,columns = headers)

expt_data_df.to_csv("C:/Users/praty/Desktop/FYP-code/data.csv", index = False)