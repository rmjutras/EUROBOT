import bisect
class WeightedList:
    """Implements a list where each object appears a number of times.
    Initialization is done with a dict where keys are entries in this list and
    values are how many times that object appears."""
    
    def __init__(self, items):
        self.indexes = []
        self.items = []
        accumulator = 0
        for key in sorted(items):
            val = items[key]
            self.indexes.append(accumulator)
            self.items.append(key)
            accumulator += val

        self.len = accumulator

    def __getitem__(self, n):
        if n < 0:
            n = self.len + n
        if n < 0 or n >= self.len:
            raise IndexError

        idx = bisect.bisect_right(self.indexes, n)
        return self.items[idx-1]

    def __len__(self):
        return self.len
