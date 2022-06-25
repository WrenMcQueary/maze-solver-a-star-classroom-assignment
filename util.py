"""Other helpful classes and functions for the student to use."""


class MinPriorityQueue:
    """Minimum-priority-first priority queue.  Not a computationally efficient implementation, but totally fine for
    this project.
    """

    def __init__(self):
        self.queue = []  # Element 0 is the front of the queue

    def enqueue(self, data, priority: int) -> None:
        """Place some data into the queue with a given priority"""
        # Handle errors
        # priority not an int or float
        if not isinstance(priority, int):
            raise TypeError("priority must be an integer or float")

        self.queue.append([data, priority])

    def dequeue(self):
        """Return the data element with lowest priority, and remove it from the queue.  In case of ties, the data element earliest in the queue is
        chosen."""
        # Handle errors
        # queue empty
        if len(self.queue) == 0:
            raise RuntimeError("Cannot dequeue from an empty queue")

        lowest_priority = float("inf")
        lowest_priority_position = None
        for ii in range(len(self.queue)):
            this_priority = self.queue[ii][1]
            if this_priority < lowest_priority:
                lowest_priority_position = ii
                lowest_priority = this_priority
        removed_element = self.queue.pop(lowest_priority_position)
        return removed_element[0]
