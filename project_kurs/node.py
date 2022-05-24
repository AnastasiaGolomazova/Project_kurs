class Node():
    previous = None
    next = None
    number = None

    def __init__(self, number, next = None, previous = None, type="single"):
        self.previous = previous
        self.next = next
        self.number = number
        self.type = type
        pass

    def __str__(self) -> str:
        if self.type == "single":
            if self.next is None:   
                return f"<{self.number},None>"
            else:
                return f"<{self.number},{self.next.number}>"
        else:
            if self.previous is not None:
                if self.next is not None:
                    return f"<{self.previous.number},{self.number},{self.next.number}>"
                else:
                    return f"<{self.previous.number},{self.number},None>"
            else:
                if self.next is not None:
                    return f"<None,{self.number},{self.next.number}>"
                else:
                    return f"<None,{self.number},None>"
