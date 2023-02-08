import random
from node import Node
from message import Message
from initializer import Initializer
import math


class Master:
    def __init_nodes(self):

        nodes_map = {}

        for i in range(self.num_hosts):

            nodes_map[i] = Node(
                N=self.num_hosts,
                M=self.num_task,
                host_id=i,
                profits=self.initializer.profits,
                resource_host_storage=self.initializer.resource_host_storage,
                resource_host_bandwidth=self.initializer.resource_host_bandwidth,
                resource_host_comp=self.initializer.resource_host_comp,
                resource_task_bandwidth=self.initializer.resource_task_bandwidth,
                resource_task_comp=self.initializer.resource_task_comp,
                resource_task_storage=self.initializer.resource_task_storage,
                neighbours=self.initializer.graph[i],
            )

        return nodes_map

    def __init__(self, initializer: Initializer, iter_num=10) -> None:

        self.num_hosts = initializer.num_hosts
        self.num_task = initializer.num_task
        self.initializer = initializer
        self.nodes = self.__init_nodes()
        self.link_msg_queue = {}
        self.iter_num = iter_num

    def __add_msg_to_receiver_msg_queue(self, message: Message):

        receiver_id = message.receive_host

        receiver_node = self.nodes[receiver_id]
        receiver_node.add_message(message)

    def __return_real_bandwidth(
        self,
    ):
        min = 5
        max = 60
        step = 5
        bandwidth_list = range(min, max + step, step)

        chosen_bandwidth = random.choice(bandwidth_list)

        return chosen_bandwidth

    def __return_chosen_links(self):

        min = 5
        max = 50
        step = 5
        bandwidth_list = range(min, max + step, step)

        chosen_bandwidth = random.choice(bandwidth_list)
        print(f"Central queue Bandwidth: {chosen_bandwidth}")
        link_num = math.ceil((chosen_bandwidth / 100) * len(self.link_msg_queue.keys()))

        sampled_links = random.sample(list(self.link_msg_queue.keys()), link_num)
        print("Sampled list:")
        print(sampled_links)
        print("Actual list:")
        print(self.link_msg_queue.keys())
        return sampled_links

    def __deliver_messages(self):
        iter_list = self.__return_chosen_links()

        for link in iter_list:

            chosen_bandwidth = self.__return_real_bandwidth()
            deliver_msg_num = math.ceil((chosen_bandwidth / 100) * len(self.link_msg_queue[link]))

            if deliver_msg_num <= len(self.link_msg_queue[link]):
                for i in range(deliver_msg_num):

                    msg = self.link_msg_queue[link].pop(0)
                    self.__add_msg_to_receiver_msg_queue(msg)

    def __add_msg_to_central_queue(self, msg: Message):

        sent_by = msg.sent_host
        received_by = msg.receive_host

        if (sent_by, received_by) not in self.link_msg_queue:
            self.link_msg_queue[(sent_by, received_by)] = [msg]
        else:
            self.link_msg_queue[(sent_by, received_by)].append(msg)

    def count_of_central_queue(self):

        cnt = 0

        for msg_list in self.link_msg_queue.values():

            cnt += len(msg_list)

        return cnt

    def count_of_all_queues(self):

        cnt = 0

        for node in self.nodes.values():

            cnt += len(node.message_queue)

        return cnt

    def phase_1(
        self,
    ):
        cnt = 1
        while self.iter_num > 0:

            self.__deliver_messages()
            iter_list = list(self.nodes.values())
            random.shuffle(iter_list)
            for node in iter_list:
                print(
                    f"-----------Phase 1, Iter {cnt} for host {node.host_id}----------"
                )
                node.receive()
                send_msg_list = node.send()
                for msg in send_msg_list:

                    self.__add_msg_to_central_queue(msg)
                print(
                    f"---------------------------------------------------------------"
                )
            self.iter_num -= 1
            print(self.link_msg_queue)
            cnt += 1

    def __init_phase_2(self):
        self.link_msg_queue = {}

        for node in self.nodes.values():

            node.init_agreement_phase()
            send_msg_list = node.send()

            for msg in send_msg_list:

                self.__add_msg_to_central_queue(msg)

    def phase_2(
        self,
    ):

        # clearing the central message queue

        self.__init_phase_2()

        while self.count_of_central_queue() > 0 or self.count_of_all_queues() > 0:

            self.__deliver_messages()

            iter_list = list(self.nodes.values())
            random.shuffle(iter_list)
            for node in iter_list:
                print(f"-----------Phase 1, host {node.host_id}----------")
                node.agree()
                send_msg_list = node.send()

                for msg in send_msg_list:

                    self.__add_msg_to_central_queue(msg)

            print(self.count_of_central_queue())

    def print(
        self,
    ):

        for node in self.nodes.values():
            print(f"-----------Final solution for host {node.host_id}----------")

            print(node.ant_colony.best_prof)
            print(node.timestamp)
            print(f"---------------------------------------------------------------")
