from timestamp import Timestamp


class Message:
    def __init__(self, sent_by, received_by, timestamp: Timestamp) -> None:

        self.sent_host = sent_by
        self.receive_host = received_by
        self.timestamp = timestamp


class Phermone_message(Message):
    def __init__(
        self, sent_by, received_by, phermone_dict: dict, timestamp: Timestamp
    ) -> None:
        super().__init__(sent_by, received_by, timestamp=timestamp)

        self.phermone_dictionary = phermone_dict


class Agreement_message(Message):
    def __init__(
        self, sent_by, received_by, timestamp: Timestamp, solution, profit
    ) -> None:
        super().__init__(sent_by, received_by, timestamp=timestamp)

        self.solution = solution
        self.profit = profit


class First_phase_completed_message(Message):
    def __init__(self, received_by, timestamp) -> None:
        super().__init__(None, received_by, timestamp)
