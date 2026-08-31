class TicketIDGenerator:
    """
        Generates unique Ticket IDs.
        """
    def __init__(self):
        self.current_id = 1

    def next_id(self):
        ticket_id = self.current_id
        self.current_id += 1
        return ticket_id

generator = TicketIDGenerator()

for _ in range(5):
    print(generator.next_id())