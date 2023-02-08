"""
Each host is a node or agent to run the distributed algorithm
"""
from timestamp import Timestamp
from ant_colony import Ant_colony
from message import (
    Phermone_message,
    Message,
    Agreement_message,
    First_phase_completed_message,
)
import copy


class Node:
    def __init__(
        self,
        N,
        M,
        host_id,
        profits,
        resource_host_storage,
        resource_host_comp,
        resource_host_bandwidth,
        resource_task_storage,
        resource_task_comp,
        resource_task_bandwidth,
        neighbours=[],
        n_ants=2,
        n_iterations=4,
        decay=0.2,
        alpha=0.85,
        beta=0.5,
    ) -> None:
        self.num_hosts = N
        self.num_tasks = M
        self.host_id = host_id
        self.ant_colony = Ant_colony(
            profits=profits,
            n_ants=n_ants,
            n_iterations=n_iterations,
            alpha=alpha,
            beta=beta,
            decay=decay,
        )
        self.first_run = True
        self.neighbours = neighbours
        self.message_queue = []
        self.send_messages_list = []
        self.resource_host_storage = resource_host_storage
        self.resource_host_comp = resource_host_comp
        self.resource_host_bandwidth = resource_host_bandwidth
        self.resource_task_storage = resource_task_storage
        self.resource_task_comp = resource_task_comp
        self.resource_task_bandwidth = resource_task_bandwidth
        self.timestamp = Timestamp(self.num_hosts)
        self.world_info_phermone = {}
        self.world_info_last_message_timestamp = {}
        self.__init_world_info()

    def __init_world_info(self):

        self.world_info_phermone[self.host_id] = self.ant_colony.phermones
        self.world_info_last_message_timestamp[self.host_id] = self.timestamp

    def __calculate_weight(self, message_timestamp: Timestamp):

        logical_clock_sum = 0

        for host_id in self.world_info_last_message_timestamp:

            logical_clock_sum += sum(self.world_info_last_message_timestamp[host_id])

        weight = sum(message_timestamp) / logical_clock_sum

        return weight

    def __update_world_info(self, message: Phermone_message):

        print(f"Host timestamp: {self.timestamp.arr}")
        print(f"Message timestamp: {message.timestamp.arr}")

        for host_id in range(self.num_hosts):

            if host_id in message.phermone_dictionary:
                if (
                    message.timestamp[host_id] > self.timestamp[host_id]
                    and host_id != self.host_id
                ):

                    print(f"Updating World information for {host_id}")

                    self.world_info_phermone[host_id] = message.phermone_dictionary[
                        host_id
                    ]
                    self.world_info_last_message_timestamp[host_id] = message.timestamp

    def __update_timestamp(self, message: Message = None):

        if message is not None:
            for i in range(self.num_hosts):

                self.timestamp[i] = max(self.timestamp[i], message.timestamp[i])

        self.timestamp[self.host_id] += 1

    def __handle_phermone_message(self, message: Phermone_message):

        world_info_count = len(self.world_info_last_message_timestamp.keys())
        print(f"World Info count:{world_info_count}")
        if world_info_count < 3:

            weight = 1 / self.num_hosts
        else:

            weight = self.__calculate_weight(message_timestamp=message.timestamp)
        print(f"Weight of the update = {weight}")
        print("Old phermone value")
        print(self.ant_colony.phermones)
        print(f"Merging phermone values of {self.host_id} with {message.sent_host}")
        self.ant_colony.merge_phermone(
            message_phermone=message.phermone_dictionary[message.sent_host],
            weight=weight,
        )
        print("Updated Phermone value")
        print(self.ant_colony.phermones)
        print(f"Performing Ant colony Optimization with new phermones")
        self.ant_colony.main(
            resource_host_bandwidth=self.resource_host_bandwidth,
            resource_host_storage=self.resource_host_storage,
            resource_host_comp=self.resource_host_comp,
            resource_task_bandwidth=self.resource_task_bandwidth,
            resource_task_storage=self.resource_task_storage,
            resource_task_comp=self.resource_task_comp,
        )
        self.__update_world_info(message=message)
        self.__update_timestamp(message=message)
        self.__add_phermone_message()

    def __handle_agreement_message(self, message: Agreement_message):

        profit = message.profit
        solution = message.solution

        if profit > self.ant_colony.best_prof:

            self.ant_colony.best_prof = profit
            self.ant_colony.best_solution = solution
            self.__update_timestamp(message=message)
            self.__add_agreement_message()

    def __add_agreement_message(self):

        messages = []
        for neighbour in self.neighbours:

            msg = Agreement_message(
                sent_by=self.host_id,
                received_by=neighbour,
                timestamp=self.timestamp,
                solution=self.ant_colony.best_solution,
                profit=self.ant_colony.best_prof,
            )

            messages.append(msg)

        self.send_messages_list += messages

    def __add_phermone_message(
        self,
    ):

        messages = []
        for neighbour in self.neighbours:

            msg = Phermone_message(
                sent_by=self.host_id,
                received_by=neighbour,
                phermone_dict=self.world_info_phermone,
                timestamp=self.timestamp,
            )

            messages.append(msg)

        self.send_messages_list += messages

    def __check_intended_recipient(self, message: Message):

        if message.receive_host is self.host_id:

            return True

        return False

    def __handle_no_message(
        self,
    ):
        if self.first_run:
            self.ant_colony.main(
                resource_host_bandwidth=self.resource_host_bandwidth,
                resource_host_storage=self.resource_host_storage,
                resource_host_comp=self.resource_host_comp,
                resource_task_bandwidth=self.resource_task_bandwidth,
                resource_task_storage=self.resource_task_storage,
                resource_task_comp=self.resource_task_comp,
            )
            self.__update_timestamp()
            self.__add_phermone_message()
            self.first_run = False
        

    def add_message(self, message: Message):

        self.message_queue.append(message)

    def send(self):
        send_messages = copy.deepcopy(self.send_messages_list)
        self.send_messages_list = []
        return send_messages

    def receive(self):

        if len(self.message_queue) == 0:
            print("Message queue is empty!!")
            self.__handle_no_message()
            return

        message = self.message_queue.pop(0)

        if not self.__check_intended_recipient(message):

            print(
                f"Message not intended for host id {self.host_id} instead its for {message.receive_host}"
            )
            return

        if message.timestamp < self.timestamp:
            print("Timestamp of the message is very old")
            return

        if type(message) is Phermone_message:

            print(f"Receieved Phermone message from {message.sent_host}")
            self.__handle_phermone_message(message)

        elif type(message) is First_phase_completed_message:
            pass
        else:

            print("Invalid message type")

    def init_agreement_phase(self):

        self.__add_agreement_message()
        self.message_queue = []

    def agree(self):

        if len(self.message_queue) == 0:
            print("Message queue is empty!!")
            return

        message = self.message_queue.pop(0)

        if type(message) is Agreement_message:

            print(f"Receieved Agreement message from {message.sent_host}")

            self.__handle_agreement_message(message)
