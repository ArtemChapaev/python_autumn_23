class LRUCache:

    def __init__(self, limit=42):
        if not isinstance(limit, int):
            raise TypeError("int required")
        if limit <= 0:
            raise ValueError("limit must be positive number")

        self.limit = limit
        # will use property that dictionary's keys are ordered
        self.cache = {}

    def get(self, key):
        value = self.cache.get(key)
        if value is None:
            return None

        # update current key
        del self.cache[key]
        self.cache[key] = value

        return value

    def set(self, key, value):
        if self.cache.get(key) is None and len(self.cache) >= self.limit:
            # get first key from cache
            # bcs we always update key, first key is last used
            last_used_key = next(iter(self.cache))
            del self.cache[last_used_key]
        elif not self.cache.get(key) is None:
            # update current key
            del self.cache[key]

        self.cache[key] = value
