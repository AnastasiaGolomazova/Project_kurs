class Node():
    previous = None
    next = None

    def __init__(self, number, next = None, previous = None):
        self.previous = previous
        self.next = next
        self.number = number
        pass

    def __str__(self) -> str:
        if self.previous is not None:
            return f"<{self.previous.number},{self.number},{self.next.number}>"
        else:
            if self.next is None:   
                return f"<{self.number},None>"
            else:
                return f"<{self.number},{self.next.number}>"